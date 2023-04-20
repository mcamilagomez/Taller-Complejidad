from main import grafo
import pandas as pd
import folium
import os
def Update_Map(Aristas: list):

    vuelos = pd.read_csv('data/totalvuelos.csv')
    map = folium.Map(location=[4.570868,-74.297333],zoom_start=6)
    for index, location_info in vuelos.iterrows():
       folium.Marker([location_info["lat_st"], location_info["lng_st"]], popup=location_info["Ciudad_Origen"], icon=folium.Icon(color="pink", icon="plane")).add_to(map)

    graph = grafo.MatrizAdy()

    for i in range(len(Aristas)):
        node1 = grafo.listavertices[i]
        node2 = grafo.listavertices[Aristas[i]]
        weight = graph[i][Aristas[i]]
        folium.vector_layers.PolyLine([(node1.lat, node1.long), (node2.lat, node2.long)], color="purple", weight=3, tooltip=str(weight)).add_to(map)

    directory = r"app/static"
    Save = os.path.join(directory, "map.html")
    map.save(Save)

