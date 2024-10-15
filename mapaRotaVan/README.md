# Projeto de Rotas com OR-Tools e OSRM

Este projeto utiliza a biblioteca OR-Tools do Google para otimizar rotas com base em coordenadas geográficas fornecidas. O principal objetivo é determinar a ordem ideal para visitar uma série de pontos, reduzindo assim a distância total percorrida. Além disso, a biblioteca OSRM (Open Source Routing Machine) é utilizada para calcular as rotas entre essas coordenadas, garantindo que as trajetórias sejam eficientes e precisas. Todas as ferramentas utilizadas são gratuitas, tornando este projeto acessível para desenvolvedores e entusiastas que desejam implementar soluções de roteamento em suas aplicações.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para o desenvolvimento.
- **FastAPI**: Framework web para construir APIs rápidas.
- **OR-Tools**: Biblioteca para resolver problemas de otimização, incluindo roteamento.
- **Folium**: Biblioteca para visualização de dados geográficos em mapas.
-  **OSRM**: Biblioteca para calcular as rotas

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio
   
2. Crie um ambiente virtual e ative-o:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate  # Para Windows

3. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt

## Uso
1. Para iniciar o servidor FastAPI, execute:

   ```bash
   uvicorn main:app --reload
   
## Referências
- [Documentação do OR-Tools - Problema de Roteamento](https://developers.google.com/optimization/routing/vrp?hl=pt-br)
- [Documentação da API do OSRM](https://project-osrm.org/docs/v5.24.0/api/#)
- [Documentação da Folium]([https://project-osrm.org/docs/v5.24.0/api/#](https://python-visualization.github.io/folium/latest/user_guide/map.html))

