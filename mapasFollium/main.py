from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import folium
import json

app = FastAPI()

coordenadas_limites = [
    [-25.0025, -53.4501],
    [-25.0031, -53.4498],
    [-25.0035, -53.4494],
    [-25.0041, -53.4490],
    [-25.0044, -53.4486],
    [-25.0043, -53.4480],
    [-25.0041, -53.4471],
    [-25.0032, -53.4473],
    [-25.0026, -53.4466],
    [-25.0024, -53.4472],
    [-25.0020, -53.4479],
    [-25.0021, -53.4492]
]

@app.get("/", response_class=HTMLResponse)
async def display_map():
    # Coordenadas para a localização de origem
    lat_org = -24.957777  
    long_org = -53.459028

    # Carregar dados dos sensores
    try:
        with open('sensors_data.json', 'r') as f:
            sensores = json.load(f)
    except Exception as e:
        return HTMLResponse(content=f"Erro ao carregar dados dos sensores: {str(e)}", status_code=500)

    # Criação do mapa centralizado na localização fornecida
    folium_map = folium.Map(location=[lat_org, long_org], tiles='cartodb positron', zoom_start=13)

    ######## Camadas para as informações ########
    # Camada para a área da lavoura
    area_layer = folium.FeatureGroup(name='Área da Lavoura').add_to(folium_map)
    # Camada para os marcadores de sensores
    sensors_layer = folium.FeatureGroup(name='Sensores').add_to(folium_map)
    # Camada para os círculos de baixa umidade
    low_moisture_layer = folium.FeatureGroup(name='Círculos de Baixa Umidade').add_to(folium_map)
    #############################################

    # Definindo a cor da área da lavoura
    folium.Polygon(
        locations=coordenadas_limites,
        color="green",  # Cor da borda da área da lavoura
        fill=True,
        fill_color="lightgreen",  # Cor de preenchimento da área da lavoura
        weight=5,
        opacity=0.5
    ).add_to(area_layer)

    # Adicionando os pontos dos sensores no mapa
    for sensor in sensores:
        try:
            latitude = sensor["coordenadas"]["latitude"]
            longitude = sensor["coordenadas"]["longitude"]
            umidade = sensor["dados"]["umidade"]
            temperatura = sensor["dados"]["temperatura"]
            ph = sensor["dados"]["ph"]
            nutrientes = sensor["dados"].get("nutrientes", {})

            # Definindo a cor com base nos dados do sensor
            cor = validaFaixaDados(umidade, temperatura, ph)

            # Definindo conteúdo do popup com informações dos sensores
            nutrientes_html = ''.join(
                f"<li><strong>{nome.capitalize()}:</strong> {valor}</li>"
                for nome, valor in nutrientes.items()
            )

            iframe = folium.IFrame(f'''
                <p style='font-size:16px'>  
                    <strong>Umidade:</strong> {umidade}% <br>
                    <strong>Temperatura:</strong> {temperatura}°C <br>
                    <strong>pH do Solo:</strong> {ph} <br>
                    <strong>Nutrientes:</strong>
                    <ul>{nutrientes_html}</ul> 
                </p>
            ''')
            popup = folium.Popup(iframe, min_width=350, max_width=300)

            # Adicionando o marcador para o sensor
            folium.Marker(
                location=[latitude, longitude],
                icon=folium.Icon(icon='info-sign', color=cor),
                popup=popup
            ).add_to(sensors_layer)

            # Se a umidade for muito baixa, adicionar um círculo ao redor do sensor
            if umidade < 20:  # Definindo um limite para baixa umidade
                folium.Circle(
                    location=[latitude, longitude],
                    radius=25,  # Ajuste o raio conforme necessário
                    fill=True,
                    fill_opacity=0.4,  # Aumentando a opacidade do preenchimento
                    color='cornflowerblue',  # Cor da borda para baixa umidade
                    opacity=0.4,  # Opacidade da borda igual ao preenchimento
                ).add_to(low_moisture_layer)

        except KeyError as e:
            print(f"Erro ao processar sensor: {sensor}. Chave faltando: {e}")
            continue  # Ignora este sensor e continua

    # Adicionando controle de camadas
    folium.LayerControl().add_to(folium_map)

    # Renderizando o mapa como resposta HTML
    map_response = folium_map.get_root().render()
    return HTMLResponse(content=map_response, status_code=200)

def validaFaixaDados(umidade, temperatura, ph):
    cor = ""
    # Validar umidade
    if 40 <= umidade <= 60:
        cor = "green"
    elif 20 <= umidade < 40 or 60 < umidade <= 80:
        cor = "orange"
    else:
        cor = "red"

    # Validar temperatura
    if 18 <= temperatura <= 25:
        cor = "green"
    elif 10 <= temperatura < 18 or 25 < temperatura <= 30:
        cor = "orange"
    else:
        cor = "red"

    # Validar pH
    if 6.0 <= ph <= 7.5:
        cor = "green"
    elif 5.5 <= ph < 6.0 or 7.5 < ph <= 8.0:
        cor = "orange"
    else:
        cor = "red"
        
    return cor
