from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def calcular_rotas(coordenadas):
    # Criação do gerenciador de roteamento
    manager = pywrapcp.RoutingIndexManager(len(coordenadas), 1, 0)

    # Criação do modelo de roteamento
    routing = pywrapcp.RoutingModel(manager)

    # Função que calcula a distância entre os pontos
    def haversine(coord1, coord2):
        from math import radians, cos, sin, asin, sqrt

        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Raio da Terra em km
        return c * r

    # Registrar a função de distância como um callback
    def distancia_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(haversine(coordenadas[from_node], coordenadas[to_node]) * 1000)  # Convertendo para metros

    # Adicionando a função de distância
    distancia_callback_index = routing.RegisterTransitCallback(distancia_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(distancia_callback_index)

    # Definindo a estratégia de solução
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    # Solução do problema
    solution = routing.SolveWithParameters(search_parameters)

    if not solution:
        print("Não foi possível encontrar uma solução.")
        return []

    # Recuperando a rota
    index = routing.Start(0)
    route = []
    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))
        index = solution.Value(routing.NextVar(index))

    return [coordenadas[i] for i in route]
