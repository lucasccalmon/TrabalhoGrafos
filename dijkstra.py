import sys

def dijkstra_matrix(graph, src):
    """
    Implementação do Dijkstra O(V^2) baseada no slide.
    Entrada:
        graph: Matriz de adjacência (Lista de listas) onde graph[u][v] é o peso.
               0 indica ausência de aresta.
        src: Vértice de origem (inteiro).
    """
    V = len(graph)
    
    # Inicialização (Linhas 3-8 do slide)
    dist = [float('inf')] * V
    sptSet = [False] * V # Shortest Path Tree Set
    
    dist[src] = 0
    
    # Loop principal (Linha 13)
    for count in range(V - 1):
        
        # Encontrar o vértice de mínima distância que ainda não foi processado
        # (Equivalente às linhas 16-20)
        min_val = float('inf')
        min_index = -1
        
        for v in range(V):
            if not sptSet[v] and dist[v] <= min_val:
                min_val = dist[v]
                min_index = v
        
        # u é o vértice escolhido
        u = min_index
        
        # Verificação de segurança (caso o grafo seja desconexo)
        if u == -1:
            break
            
        sptSet[u] = True # Linha 24
        
        # Atualizar distâncias dos vizinhos (Linhas 26-30)
        for v in range(V):
            # A condição verifica:
            # 1. Se v não está no conjunto processado (!sptSet[v])
            # 2. Se existe aresta entre u e v (graph[u][v])
            # 3. Se a distância de u é válida (dist[u] != inf)
            # 4. Se o novo caminho é menor
            if (not sptSet[v] and 
                graph[u][v] != 0 and 
                dist[u] != float('inf') and 
                dist[u] + graph[u][v] < dist[v]):
                
                dist[v] = dist[u] + graph[u][v]

    # Impressão dos resultados (Linhas 33-34)
    print("Vértice \t Distância da Origem")
    for i in range(V):
        print(f"{i} \t\t {dist[i]}")
        
    return dist

# Configuração do Grafo da imagem 2 para Dijkstra
# Matriz 5x5 inicializada com 0
V_dijk = 5
graph_dijk = [[0 for _ in range(V_dijk)] for _ in range(V_dijk)]

# Preenchendo a matriz de adjacência (graph[u][v] = peso)
# Indices ajustados (1 vira 0, etc.)

# Arestas saindo do 1 (0)
graph_dijk[0][1] = 4  # 1 -> 2
graph_dijk[0][2] = 2  # 1 -> 3

# Arestas saindo do 2 (1)
graph_dijk[1][2] = 3  # 2 -> 3
graph_dijk[1][3] = 2  # 2 -> 4
graph_dijk[1][4] = 3  # 2 -> 5

# Arestas saindo do 3 (2)
graph_dijk[2][1] = 1  # 3 -> 2
graph_dijk[2][3] = 4  # 3 -> 4
graph_dijk[2][4] = 5  # 3 -> 5

# Arestas saindo do 4 (3)

# Arestas saindo do 5 (4)
graph_dijk[4][3] = 1  # 5 -> 4

print("\n--- Teste Dijkstra ---")
dijkstra_matrix(graph_dijk, 0)