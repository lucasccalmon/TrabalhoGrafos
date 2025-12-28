import time
import random
import sys
import pandas as pd

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



from dijkstra_artigo_corrigido import sssp_break_sorting_barrier as dijA
        






def gerar_dados_teste(num_vertices, densidade):
    """
    Gera um grafo aleatório e retorna os formatos para Dijkstra (Matriz) e BF (Lista).
    """
    max_peso = 10
    matriz = [[0] * num_vertices for _ in range(num_vertices)]
    arestas = []
    
    num_arestas = 0
    for u in range(num_vertices):
        for v in range(num_vertices):
            if u != v and random.random() < densidade:
                peso = random.randint(1, max_peso)
                matriz[u][v] = peso
                arestas.append([u, v, peso])
                num_arestas += 1
                
    return matriz, arestas, num_arestas


def rodar_benchmark_completo():
    print("Iniciando Benchmark Completo (3 Algoritmos)...")
    
    # Configurações
    NUM_RODADAS = 5 
    cenarios = [
        # (Vértices, Densidade)
        (50, 0.2), 
        (50, 0.8), 
        (100, 0.2), 
        (100, 0.5), 
        (100, 0.8), 
        (200, 0.2),
        (300, 0.1), # Cuidado com BF em grafos grandes!
        # --- Zona de Confirmação (V um pouco maior) ---
        (400, 0.05),  # V=400. Esparso. Dijkstra começa a sentir o peso de V^2.
        (500, 0.02),  # V=500. Muito esparso (Avg degree ~10). 
                    # Dijkstra processa 250.000 células. Artigo processa ~5.000 arestas.
        
        # --- Zona de Domínio do Artigo (V Grande) ---
        (1000, 0.01), # V=1000. Densidade 1%.
                    # Dijkstra: 1.000.000 operações na matriz.
                    # Artigo: ~10.000 arestas. Diferença deve ser brutal aqui.

        # --- O "Grand Finale" (Se sua máquina aguentar) ---
        (2000, 0.005) # V=2000. Densidade 0.5%.
                    # Dijkstra: 4.000.000 operações. Vai demorar bastante (>400ms provável).
                    # Artigo: ~20.000 arestas. Deve se manter rápido (<20ms).
    ]
    
    resultados_brutos = []

    for V, densidade in cenarios:
        print(f"Processando V={V}, Densidade={densidade}...")
        
        for rodada in range(NUM_RODADAS):
            # 1. Gerar dados (Matriz e Listas)
            matriz, arestas, E = gerar_dados_teste(V, densidade)
            src = 0
            
            # Converter para Lista de Adjacência (Necessário para o Dijkstra Faixas)
            adj_list = [[] for _ in range(V)]
            for u, v, w in arestas:
                adj_list[u].append((v, w))
            
            # --- Teste 1: Dijkstra Clássico (Matriz) ---
            start = time.perf_counter()
            dijkstra_matrix(matriz, src)
            t_classico = (time.perf_counter() - start) * 1000

            # --- Teste 2: Bellman-Ford ---
            start = time.perf_counter()
            bellman_ford_edgelist(arestas, V, E, src)
            t_bf = (time.perf_counter() - start) * 1000
            
            # --- Teste 3: Dijkstra Artigo (Faixas) ---
            # Definimos delta como uma média simples dos pesos (ex: 2 ou 5)
            start = time.perf_counter()
            dijA(adj_list, 0)
            t_artigo = (time.perf_counter() - start) * 1000
            
            resultados_brutos.append({
                "Vértices": V,
                "Densidade": densidade,
                "Arestas": E,
                "Dijkstra Clássico (ms)": t_classico,
                "Artigo (ms)": t_artigo,
                "Bellman-Ford (ms)": t_bf,
            })

    # Criar DataFrame e Média
    df = pd.DataFrame(resultados_brutos)
    df_final = df.groupby(["Vértices", "Densidade"]).mean(numeric_only=True).reset_index()
    
    # Remover colunas desnecessárias para visualização limpa
    cols = ["Vértices", "Densidade", "Arestas", "Dijkstra Clássico (ms)", "Artigo (ms)", "Bellman-Ford (ms)" ]
    print("\n" + "="*80)
    print("RESULTADOS FINAIS - MÉDIA DE TEMPO")
    print("="*80)
    print(df_final[cols].to_string(index=False))
    
    return df, df_final

# Para rodar:
df3, df4 = rodar_benchmark_completo()

print(df3)
print("= " * 10)
print(df4)
df3.to_csv("resultados_brutos.csv", index=False)
df4.to_csv("resultados_media.csv", index=False)