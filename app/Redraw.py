from main import grafo
import pandas as pd
import folium
import os
def Update_Map_Prim(Aristas: list):

    vuelos = pd.read_csv('data/totalvuelos.csv')
    map = folium.Map(location=[4.570868,-74.297333],zoom_start=6)
    for index, location_info in vuelos.iterrows():
       folium.Marker([location_info["lat_st"], location_info["lng_st"]], popup=location_info["Ciudad_Origen"], icon=folium.Icon(color="pink", icon="plane")).add_to(map)

    for edge in Aristas:
        node1 = grafo.listavertices[edge[0]]
        node2 = grafo.listavertices[edge[1]]
        weight = edge[2]
        folium.vector_layers.PolyLine([(node1.lat, node1.long), (node2.lat, node2.long)], color="red", weight=3, tooltip=f"{str(weight)} km").add_to(map)

    directory = r"app/static"
    Save = os.path.join(directory, "map.html")
    map.save(Save)

def Update_Map_Kruskal(Aristas: list):
    vuelos = pd.read_csv('data/totalvuelos.csv')
    map = folium.Map(location=[4.570868,-74.297333],zoom_start=6)
    for index, location_info in vuelos.iterrows():
       folium.Marker([location_info["lat_st"], location_info["lng_st"]], popup=location_info["Ciudad_Origen"], icon=folium.Icon(color="pink", icon="plane")).add_to(map)

    for edge in Aristas:
        node1 = grafo.listavertices[edge[0]]
        node2 = grafo.listavertices[edge[1]]
        weight = edge[2]
        folium.vector_layers.PolyLine([(node1.lat, node1.long), (node2.lat, node2.long)], color="purple", weight=3, tooltip=f"{str(weight)} km").add_to(map)

    directory = r"app/static"
    Save = os.path.join(directory, "map.html")
    map.save(Save)