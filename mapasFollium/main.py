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
    folium_map = folium.Map(location=[lat_org, long_org], zoom_start=13)

    kw = {
        "color": "blue",
        "fill": True,
        "fill_color": "red",
        "weight": 5
    }
    
    dx = 0.012
    folium.Polygon(
        locations=coordenadas_limites,
        **kw,
    ).add_to(folium_map)
    
    # Adicionando os pontos dos sensores no mapa
    for sensor in sensores:
        try:
            latitude = sensor["coordenadas"]["latitude"]
            longitude = sensor["coordenadas"]["longitude"]
            umidade = sensor["dados"]["umidade"]
            temperatura = sensor["dados"]["temperatura"]
            ph = sensor["dados"]["ph"]
            nutrientes = sensor["dados"].get("nutrientes", {})
            
            cor = validaFaixaDados(umidade, temperatura, ph)

            nutrientes_html = ''.join(
                f"<li><strong>{nome.capitalize()}:</strong> {valor}</li>"
                for nome, valor in nutrientes.items()
            )
            # Definindo conteúdo do popup com informações dos sensores
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
            ).add_to(folium_map)

        except KeyError as e:
            print(f"Erro ao processar sensor: {sensor}. Chave faltando: {e}")
            continue  # Ignora este sensor e continua

    # Adicionando a biblioteca Font Awesome
    folium_map.get_root().html.add_child(folium.Element(
        "<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'>"
    ))
    
    # Criando a legenda HTML
    legend_html = '''
        <div id='maplegend' class='maplegend' 
            style='position: fixed; 
                   bottom: 50px; left: 50px; 
                   width: 200px; height: auto; 
                   background-color: white; 
                   border:2px solid grey; 
                   z-index:9999; 
                   font-size:14px;
                   padding: 10px;'>
            <strong>Legenda</strong><br>
            <i class="fa fa-square" style="color:green;"></i> OK <br>
            <i class="fa fa-square" style="color:orange;"></i> VERIFICAR <br>
            <i class="fa fa-square" style="color:red;"></i> RUIM
        </div>
    '''

    # Adicionando a legenda ao mapa
    folium_map.get_root().html.add_child(folium.Element(legend_html))

    # Renderizando o mapa como resposta HTML
    map_response = folium_map.get_root().render()
    return HTMLResponse(content=map_response, status_code=200)


@app.get("/display_video", response_class=HTMLResponse)
async def display_video():
    # HTML para exibir o vídeo
    video_html = '''
        <video width="100%" height="auto" controls autoplay loop>
            <source src="https://www.mapbox.com/bites/00188/patricia_nasa.webm" type="video/webm">
        </video>
    '''
    
    return HTMLResponse(content=video_html, status_code=200)



# criar uma área redonda azul com opacidade
# m = folium.Map(location=[-27.5717, -48.6256], zoom_start=9)

# radius = 50
# folium.CircleMarker(
#     location=[-27.55, -48.8],
#     radius=radius,
#     color="cornflowerblue",
#     stroke=False,
#     fill=True,
#     fill_opacity=0.6,
#     opacity=1,
#     popup="{} pixels".format(radius),
#     tooltip="I am in pixels",
# ).add_to(m)



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
