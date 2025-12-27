def bellman_ford_edgelist(graph_edges, V, E, src):
    """
    Implementação do Bellman-Ford baseada no slide.
    Entrada:
        graph_edges: Lista de arestas, onde cada item é [u, v, w].
        V: Número de vértices.
        E: Número de arestas.
        src: Vértice de origem.
    """
    
    # Inicialização (Linhas 3-7)
    dis = [float('inf')] * V
    dis[src] = 0
    
    # Relaxamento das arestas V-1 vezes (Linhas 9-15)
    for i in range(V - 1):
        for j in range(E):
            u = graph_edges[j][0]
            v = graph_edges[j][1]
            w = graph_edges[j][2]
            
            # Verifica se podemos melhorar o caminho para v passando por u
            if dis[u] != float('inf') and dis[u] + w < dis[v]:
                dis[v] = dis[u] + w

    # Verificação de Ciclo Negativo (Linhas 17-25)
    for i in range(E):
        x = graph_edges[i][0]
        y = graph_edges[i][1]
        weight = graph_edges[i][2]
        
        if dis[x] != float('inf') and dis[x] + weight < dis[y]:
            print("Grafo contém ciclo de tamanho negativo")
            return # Encerra se achar ciclo negativo

    # Impressão dos resultados (Linhas 27-29)
    print("Distância do vértice até a origem")
    for i in range(V):
        print(f"{i} \t\t {dis[i]}")
        
    return dis

# Configuração do Grafo da imagem 1 para Bellman-Ford
V_bf = 6  # Total de vértices (1 a 6)
E_bf = 8  # Total de arestas
src_bf = 0 # Vértice de origem (1 na imagem virou 0)

# Lista de Arestas [origem, destino, peso]
# Ajustado para índices começando em 0
edges_bf = [
    [0, 5, 8],   # 1 -> 6 (peso 8)
    [0, 1, 10],  # 1 -> 2 (peso 10)
    [5, 4, 1],   # 6 -> 5 (peso 1)
    [4, 1, -4],  # 5 -> 2 (peso -4)
    [4, 3, -1],  # 5 -> 4 (peso -1)
    [1, 3, 2],   # 2 -> 4 (peso 2) -> Assumindo a seta diagonal descendo
    [3, 2, -2],  # 4 -> 3 (peso -2)
    [2, 1, 1]    # 3 -> 2 (peso 1)
]

print("--- Teste Bellman-Ford ---")
bellman_ford_edgelist(edges_bf, V_bf, E_bf, src_bf)