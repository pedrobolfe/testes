from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import folium
import json
import httpx
from typing import List, Dict, Any
from otimizarRota import calcular_rotas

app = FastAPI()

async def get_route(coordenadas):
    locations = ';'.join(coordenadas)
    url_osrm = f"http://router.project-osrm.org/route/v1/driving/{locations}?geometries=geojson"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url_osrm)
        if response.status_code != 200:
            print(f"erro na requisicao para osrm: {response.status_code} - {response.text}")
            return {}
        return response.json()


@app.get("/", response_class=HTMLResponse)
async def display_map():
    # Coordenadas para a localização de origem e destino
    lat_org, long_org = -24.978461778505483, -53.46487601296926 
    lat_dest, long_dest = -24.916591929080333, -53.4176426664389
    
    try:
        with open('dados.json', 'r') as f:
            enderecos = json.load(f)
    except Exception as e:
        return HTMLResponse(content=f"Erro ao carregar dados: {str(e)}", status_code=500)

    coordenadas = calcular_rotas([endereco['coordenadas'] for endereco in enderecos])
    
    # Criação do mapa
    folium_map = folium.Map(location=[lat_org, long_org], tiles='cartodb positron', zoom_start=13)

    # Ponto inicial
    add_marcador([lat_org, long_org], "Ponto Inicial", "green").add_to(folium_map)
    route = await get_route([f"{long_org},{lat_org}", f"{coordenadas[0][1]},{coordenadas[0][0]}"])
    route_coords = route['routes'][0]['geometry']['coordinates']
    add_linha_rota(route_coords, "Rota Inicial", "darkgreen").add_to(folium_map)
    
    for i in range(len(coordenadas) - 1):
        route = await get_route([f"{coordenadas[i][1]},{coordenadas[i][0]}", f"{coordenadas[i + 1][1]},{coordenadas[i + 1][0]}"])

        # Adicionar marcadores
        add_marcador([coordenadas[i][0], coordenadas[i][1]], enderecos[i]['nome'], "blue").add_to(folium_map)

        # Traçar a rota no mapa
        route_coords = route['routes'][0]['geometry']['coordinates']
        add_linha_rota(route_coords, "Rota aos endereços dos alunos", "gray").add_to(folium_map)
        
    # Adicionando o ponto final
    add_marcador([coordenadas[-1][0], coordenadas[-1][1]], enderecos[-1]['nome'], "blue").add_to(folium_map)
    
    # Destino 
    route = await get_route([f"{long_dest},{lat_dest}", f"{coordenadas[-1][1]},{coordenadas[-1][0]}"])
    route_coords = route['routes'][0]['geometry']['coordinates']
    add_linha_rota(route_coords, "Rota final", "red").add_to(folium_map)

    # Adicionando o ponto final
    add_marcador([lat_dest, long_dest], "Ponto Final", "red").add_to(folium_map)
    
    map_response = folium_map._repr_html_()
    return HTMLResponse(content=map_response, status_code=200)


def add_marcador(coordenadas, nome, color):
    return folium.Marker(
        location=coordenadas,
        popup=nome,
        tooltip=nome,
        icon=folium.Icon(icon='info-sign', color=color),
        shadow=False
    )

def add_linha_rota(route_coords, frase, color="blue"):
    return folium.PolyLine(
        locations=[[point[1], point[0]] for point in route_coords],
        tooltip=frase,
        color=color,
        weight=5,
        opacity=0.5
    )
