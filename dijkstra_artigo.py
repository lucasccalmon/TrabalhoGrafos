import math

def dijkstra_simplified_bands(adj_list, V, src, delta=2):
    """
    Versão Corrigida: Remove o return prematuro.
    """
    dist = [float('inf')] * V
    dist[src] = 0
    
    buckets = {} 
    buckets[0] = {src}
    
    current_bucket_idx = 0
    max_dist_seen = 0
    
    while True:
        # 1. Encontrar o próximo balde não vazio
        while current_bucket_idx not in buckets or not buckets[current_bucket_idx]:
            current_bucket_idx += 1
            
            # Condição de Parada: Se passamos da maior distância vista e não tem mais nada
            if current_bucket_idx * delta > max_dist_seen:
                is_empty = True
                for k in buckets:
                    if k >= current_bucket_idx and buckets[k]:
                        is_empty = False; break
                if is_empty: 
                    return dist # <--- O ÚNICO RETURN DEVE SER AQUI (ou na checagem de segurança)
            
            # Break de segurança para loops infinitos em grafos desconexos/estranhos
            if current_bucket_idx > V * 100 + max_dist_seen: 
                 return dist 
        
        # 2. Processar a "Faixa" (Bucket) atual
        # Enquanto houver vértices neste balde, processa
        while buckets.get(current_bucket_idx):
            u = buckets[current_bucket_idx].pop() 
            
            for v, weight in adj_list[u]:
                new_dist = dist[u] + weight
                
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    max_dist_seen = max(max_dist_seen, new_dist)
                    
                    new_bucket_idx = int(new_dist // delta)
                    
                    if new_bucket_idx not in buckets:
                        buckets[new_bucket_idx] = set()
                    
                    buckets[new_bucket_idx].add(v)
        
        # REMOVIDO O RETURN DIST QUE ESTAVA AQUI
    
# --- Cole aqui a função dijkstra_simplified_bands que já implementamos ---
# (Se precisar dela novamente, me avise que eu reenvio)

# 1. Montar a Lista de Adjacência (Entrada)
V = 5
src = 0 # Origem (Vértice 1)

adj_list = [
    [(1, 4), (2, 2)],          # Vizinhos do 0 (1)
    [(2, 3), (3, 2), (4, 3)],  # Vizinhos do 1 (2)
    [(1, 1), (3, 4), (4, 5)],  # Vizinhos do 2 (3)
    [],                        # Vizinhos do 3 (4) - Sem saída
    [(3, 1)]                   # Vizinhos do 4 (5)
]

# 2. Executar o Algoritmo
# Delta=2 é um bom valor para pesos pequenos (1 a 5) como os seus
distancias = dijkstra_simplified_bands(adj_list, V, src, delta=2)

# 3. Mostrar Resultado
print("--- Resultado Dijkstra Faixas ---")
print("Vértice \t Distância Mínima")
for i, d in enumerate(distancias):
    print(f"{i+1} \t\t {d}")