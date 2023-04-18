import folium
import pandas as pd
import webbrowser
import Redraw as R
from flask import Flask, render_template, request
import os
"""Creación del grafo"""
class Node:
    def __init__(self, data: str) -> None:
        # Nombre de la ciudad
        self.data = data
        # Lista de nodos a los cuales tiene conexión
        self.connections: list[Node] = []
        # Lista de pesos (Cada index corresponde al del nodo en connections)
        self.weights: list[float] = []
        # Posición que ocupa en la matriz de distancia
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
        self.MatrizDis: list[list[int]]
        self.MatrizRec: list[list[Node]]

    def MatrizDistancia(self) -> list[list[int]]:
        """Crea la matriz de distancia inicial (Si existe arista el peso, si no infinito)"""
        Matriz = []
        length = len(self.listavertices)
        for i in range(length):
            Fila = []
            for j in range(length):
                Fila.append(float("inf"))
            Matriz.append(Fila)
        for i in range(length):
            Matriz[i][i] = 0
        for vertice in self.listavertices:
            for conexion in vertice.connections:
                Matriz[vertice.pos][conexion.pos] = vertice.weights[vertice.connections.index(conexion)]
        return Matriz

    def MatrizRecorrido(self):
        """Crea la matriz de recorrido inicial"""
        Matriz = []
        length = len(self.listavertices)
        for i in range(length):
            Fila = []
            for j in range(length):
                Fila.append(0)
            Matriz.append(Fila)
        for vertice in self.listavertices:
            for i in range(length):
                Matriz[i][vertice.pos] = vertice
        
        return Matriz
    
    def FloydWarshall(self):
        """Ejecuta el algoritmo de Floyd-Warshall, modifica la matriz de distancia y recorrido"""
        n = len(self.listavertices)
        Matriz = self.MatrizDistancia()
        MatrizR = self.MatrizRecorrido()
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    Min = min(Matriz[i][j], Matriz[i][k] + Matriz[k][j])
                    if Min != Matriz[i][j]:
                        MatrizR[i][j] = self.listavertices[k]
                    Matriz[i][j] = Min
                    
        self.MatrizDis = Matriz
        self.MatrizRec = MatrizR

    def ListaRecorrido(self, start: str, finish: str):
        """Devuelve una lista ordenada con el recorrido más corto de un nodo a otro"""
        node1 = self.listavertices[self.listaciudades.index(start)]
        node2 = self.listavertices[self.listaciudades.index(finish)]
        lista = [node1]
        if node2 in node1.connections and self.MatrizRec[node1.pos][node2.pos] == node2:
            lista.append(node2)
        else:
            aux = node2
            path = []
            while aux not in node1.connections:
                aux = self.MatrizRec[node1.pos][aux.pos]
                path.append(aux)
            path.reverse()
            for node in path:
                lista.append(node)
            lista.append(node2)

        return lista


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


for index, info in vuelos.iterrows():
    """Iteramos nuevamente a lo largo del df para definir las adyacencias
       entre los vértices"""
    indexor = grafo.listaciudades.index(info["Ciudad_Origen"])
    indexdes = grafo.listaciudades.index(info["Ciudad_Destino"])
    
    ciudad_or = grafo.listavertices[indexor]
    ciudad_des = grafo.listavertices[indexdes]

    ciudad_or.connections.append(ciudad_des)
    ciudad_or.weights.append(round(info["distance_km"]))

# Una vez tenemos todos los datos necesarios en el grafo, llamamos
# el algorítmo de Floyd Warshall para tener la información del camino mínimo
# entre los vértices
grafo.FloydWarshall()

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
    R.Update_Map(ciudad1, ciudad2)
    #Refrescar la pagina
    return render_template('index.html')
if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000", 1)
    app.run(debug=True)
