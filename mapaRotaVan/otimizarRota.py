from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def calcular_rotas(coordenadas):
    # Criação do gerenciador de roteamento. O gerenciador é responsável por mapear as coordenadas
    # para índices que o modelo de roteamento pode usar.
    manager = pywrapcp.RoutingIndexManager(len(coordenadas), 1, 0)

    # Criação do modelo de roteamento. O modelo contém a lógica de roteamento e as variáveis.
    routing = pywrapcp.RoutingModel(manager)

    # Função que calcula a distância entre dois pontos usando a fórmula de Haversine
    def haversine(coord1, coord2):
        from math import radians, cos, sin, asin, sqrt

        # Converte as coordenadas de graus para radianos
        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])
        
        # Cálculo das diferenças de longitude e latitude
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        # Fórmula de Haversine para calcular a distância
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Raio da Terra em km
        return c * r

    # Registrar a função de distância como um callback no modelo de roteamento
    def distancia_callback(from_index, to_index):
        # Converte os índices do modelo de volta para os índices das coordenadas
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        
        # Retorna a distância entre os dois pontos, convertendo para metros
        return int(haversine(coordenadas[from_node], coordenadas[to_node]) * 1000)

    # Adiciona a função de distância ao modelo de roteamento
    distancia_callback_index = routing.RegisterTransitCallback(distancia_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(distancia_callback_index)

    # Definindo a estratégia de solução a ser utilizada
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    # Define a estratégia de solução como o "Caminho mais barato" (PATH_CHEAPEST_ARC)
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    # Soluciona o problema de roteamento
    solution = routing.SolveWithParameters(search_parameters)

    # Verifica se uma solução foi encontrada
    if not solution:
        print("Não foi possível encontrar uma solução.")
        return []

    # Recupera a rota a partir da solução
    index = routing.Start(0)  # Começa a partir do primeiro veículo (0)
    route = []
    
    # Enquanto não chegar ao fim da rota, adiciona os índices dos pontos na rota
    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))  # Converte o índice do modelo de volta para o índice original
        index = solution.Value(routing.NextVar(index))  # Move para o próximo ponto

    # Retorna as coordenadas da rota em ordem
    return [coordenadas[i] for i in route]
