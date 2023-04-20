import folium
import pandas as pd
import webbrowser
import Redraw as R
from flask import Flask, render_template, request
import os
import geopy.distance
import sys
"""Creación del grafo"""
class Node:
    def __init__(self, data: str) -> None:
        # Nombre de la ciudad
        self.data = data
        self.pos = 0
        # Latitud y longitud de la ciudad
        self.lat: float = 0
        self.long: float = 0

    def __repr__(self) -> str:
        return self.data
class Grafo:
    def __init__(self) -> None:
        # Cada elemento de la lista de vertices corresponde en su index a la de ciudades
        self.listavertices: list[Node] = []
        self.listaciudades: list[str] = []
        self.V = 0

    def MatrizAdy(self):
        Matriz = [[0 for column in range(len(self.listaciudades))]
                   for row in range(len(self.listaciudades))]

        for node in self.listavertices:
            for node2 in self.listavertices:
                Matriz[node.pos][node2.pos] = geopy.distance.geodesic((node.lat, node.long), (node2.lat, node2.long)).km

        return Matriz
    
    def minKey(self, key, mstSet):
 
        # Initialize min value
        min = sys.maxsize
 
        for v in range(self.V):
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v
 
        return min_index
 
    # Function to construct and print MST for a graph
    # represented using adjacency matrix representation
    def primMST(self):
 
        # Key values used to pick minimum weight edge in cut
        key = [sys.maxsize] * self.V
        parent = [None] * self.V  # Array to store constructed MST
        # Make key 0 so that this vertex is picked as first vertex
        key[0] = 0
        mstSet = [False] * self.V
 
        parent[0] = -1  # First node is always the root of

        graph = self.MatrizAdy()
        for cout in range(self.V):
 
            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minKey(key, mstSet)
 
            # Put the minimum distance vertex in
            # the shortest path tree
            mstSet[u] = True
 
            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
 
                # graph[u][v] is non zero only for adjacent vertices of m
                # mstSet[v] is false for vertices not yet included in MST
                # Update the key only if graph[u][v] is smaller than key[v]
                if graph[u][v] > 0 and mstSet[v] == False \
                and key[v] > graph[u][v]:
                    key[v] = graph[u][v]
                    parent[v] = u
 
        return parent

grafo = Grafo()
vuelos = pd.read_csv('data/totalvuelos.csv')
"""Iteramos a través del df y añadimos las ciudades al grafo"""
c = 0
for index, city in vuelos.iterrows():
    ciudad = city["Ciudad_Origen"]
    """Para cada ciudad que no este incluida en el grafo, definimos
       sus atributos y la incluimos a este
    """
    if ciudad not in grafo.listaciudades:
        grafo.listaciudades.append(ciudad)
        nodo = Node(ciudad)
        grafo.listavertices.append(nodo)
        nodo.pos = c
        nodo.lat = float(city["lat_st"])
        nodo.long = float(city["lng_st"])
        c += 1

grafo.V = len(grafo.listaciudades)

AristasPrim = grafo.primMST()

map = folium.Map(location=[4.570868,-74.297333],zoom_start=6)
for index, location_info in vuelos.iterrows():
    folium.Marker([location_info["lat_st"], location_info["lng_st"]], popup=location_info["Ciudad_Origen"], icon=folium.Icon(color="pink", icon="plane")).add_to(map)

# Guardamos el mapa en la carpeta requerida
directory = r"app/static"

Save = os.path.join(directory, "map.html")
map.save(Save)
#Servidor en Flask
app = Flask(__name__)
@app.route('/')
#Primera ejecución
def index():
    return render_template('pp.html')
#Para pasar a la página de los mapas
@app.route('/continuar', methods=["GET", "POST"])
def continuar():
    return render_template('index.html')
@app.route('/datos', methods=["GET", "POST"])
#Recolectar los datos
def ciudades():
    ciudad1 = request.form['city-1']
    ciudad2 = request.form['city-2']
    #Redibujar el mapa
    R.Update_Map(AristasPrim)
    #Refrescar la pagina
    return render_template('index.html')
if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000", 1)
    app.run(debug=True)
