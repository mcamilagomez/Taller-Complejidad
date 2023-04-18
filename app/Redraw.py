from main import grafo
import pandas as pd
import folium
import os
def Update_Map(start: str, finish: str):
    if start == finish:
        return
    else:
        vuelos = pd.read_csv('data/totalvuelos.csv')
        map = folium.Map(location=[4.570868,-74.297333],zoom_start=6)
        for index, location_info in vuelos.iterrows():
            if location_info["Ciudad_Origen"] == start:
                folium.Marker([location_info["lat_st"], location_info["lng_st"]], popup=location_info["Ciudad_Origen"], icon=folium.Icon(color="lightred", icon="plane")).add_to(map)
            elif location_info["Ciudad_Origen"] == finish:
                folium.Marker([location_info["lat_st"], location_info["lng_st"]], popup=location_info["Ciudad_Origen"], icon=folium.Icon(color="lightgreen", icon="plane")).add_to(map)
            else:
                folium.Marker([location_info["lat_st"], location_info["lng_st"]], popup=location_info["Ciudad_Origen"], icon=folium.Icon(color="pink", icon="plane")).add_to(map)
        if finish == "TODOS":
            lista = grafo.listavertices
            for node in lista:
                if node.data != start:
                    lista2 = grafo.ListaRecorrido(start, node.data)
                    for node1 in lista2:
                        index = lista2.index(node1)
                        if index != len(lista2) - 1:
                            node2 = lista2[lista2.index(node1) + 1]
                            weights = node1.weights[node1.connections.index(node2)]
                            folium.vector_layers.PolyLine([(node1.lat, node1.long), (node2.lat, node2.long)], color="purple", weight=3, tooltip=str(weights)).add_to(map)
        else:
            lista = grafo.ListaRecorrido(start, finish)
            for node in lista:
                index = lista.index(node)
                if index != len(lista) - 1:
                    node2 = lista[lista.index(node) + 1]
                    weights = node.weights[node.connections.index(node2)]
                    folium.vector_layers.PolyLine([(node.lat, node.long), (node2.lat, node2.long)], color="purple", weight=3, tooltip=str(weights)).add_to(map)
    
    directory = r"app/static"
    Save = os.path.join(directory, "map.html")
    map.save(Save)

