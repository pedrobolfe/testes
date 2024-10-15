# Projeto de Roteamento com OR-Tools

Este projeto utiliza a biblioteca OR-Tools do Google para otimizar rotas de entrega com base em coordenadas geográficas fornecidas. O objetivo é calcular a melhor ordem para visitar uma série de pontos, minimizando a distância total percorrida.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para o desenvolvimento.
- **FastAPI**: Framework web para construir APIs rápidas.
- **OR-Tools**: Biblioteca para resolver problemas de otimização, incluindo roteamento.
- **Folium**: Biblioteca para visualização de dados geográficos em mapas.

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


