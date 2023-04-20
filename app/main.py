import folium
import pandas as pd
import webbrowser
import Redraw as R
from flask import Flask, render_template, request
import os
import geopy.distance
import sys
import heapq
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
        

    def MatrizAdy(self):
        Matriz = [[0 for column in range(len(self.listaciudades))]
                   for row in range(len(self.listaciudades))]

        for node in self.listavertices:
            for node2 in self.listavertices:
                Matriz[node.pos][node2.pos] = round(geopy.distance.geodesic((node.lat, node.long), (node2.lat, node2.long)).km, 4)

        return Matriz
    
    
    def Prim(self) -> list[list[int]]:
        graph = self.MatrizAdy()
        n = len(graph)
        visited = [False] * n
        dist = [sys.maxsize] * n
        parent = [None] * n
    
        dist[0] = 0
        pq = [(0, 0)]
    
        while pq:
            d, u = heapq.heappop(pq)
            if visited[u]:
                continue
        
            visited[u] = True
        
            for v in range(n):
                if graph[u][v] != 0 and not visited[v] and graph[u][v] < dist[v]:
                    dist[v] = graph[u][v]
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))
                
        return [(parent[i], i, graph[i][parent[i]]) for i in range(1, n) if parent[i] is not None]

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


AristasPrim = grafo.Prim()

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
