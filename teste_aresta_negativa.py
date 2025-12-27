import time
import random
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
 #   print("Vértice \t Distância da Origem")
 #   for i in range(V):
#      print(f"{i} \t\t {dist[i]}")
        
    return dist

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
  #  print("Distância do vértice até a origem")
  #  for i in range(V):
   #     print(f"{i} \t\t {dis[i]}")
        
    return dis

def teste_aresta_negativa():
    print("\n" + "="*60)
    print("TESTE DE CORRETUDE: Arestas Negativas")
    print("="*60)
    
    # Grafo simples onde Dijkstra falha:
    # 0 -> 1 (Peso 3)
    # 0 -> 2 (Peso 4)
    # 2 -> 1 (Peso -2)
    
    V = 3
    E = 3
    src = 0
    
    # Configurar Matriz (Dijkstra)
    matriz = [[0]*V for _ in range(V)]
    matriz[0][1] = 3
    matriz[0][2] = 4
    matriz[2][1] = -2 # Aresta negativa
    
    # Configurar Lista (Bellman-Ford)
    arestas = [
        [0, 1, 3],
        [0, 2, 4],
        [2, 1, -2]
    ]
    
    print("Cenário: 0->1(2), 0->2(5), 1->2(-4)")
    print("Caminho Correto para vértice 2 deve ser: -2 (0->1->2)")
    print("-" * 40)
    
    print("Executando Dijkstra...")
    # Lembre-se de reativar os prints ou capturar o retorno da função
    dist_dijk = dijkstra_matrix(matriz, src)
    
    print("\nExecutando Bellman-Ford...")
    dist_bf = bellman_ford_edgelist(arestas, V, E, src)
    
    print("\n--- RESULTADO FINAL ---")
    print(f"Distância 0->1 pelo Dijkstra: {dist_dijk[1]} (Provavelmente Errado)")
    print(f"Distância 0->1 pelo Bellman-Ford: {dist_bf[1]} (Correto)")

# Para rodar o teste de corretude:
teste_aresta_negativa()