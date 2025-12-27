# sssp_artigo_2504_17033.py
# Implementa os Algoritmos 1, 2 e 3 de "Breaking the Sorting Barrier for Directed SSSP"
# (arXiv:2504.17033v2, Jul 2025) de forma fiel na lógica.
#
# Observação: o Lema 3.3 (estrutura parcial) é implementado aqui via heapq (prático),
# preservando a interface, mas não o tempo assintótico da prova.
#
# Grafo: adj[u] = list[(v, w)] com w >= 0 (pesos reais ou floats).

from __future__ import annotations
import math
import heapq
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set, Iterable, Optional

INF = float("inf")


@dataclass
class PredInfo:
    parent: Optional[int] = None
    w: float = 0.0  # peso da aresta (parent -> v) que gerou o db[v]


class FrontierDS:
    """
    Interface do Lema 3.3:
      - Initialize(M, B)
      - Insert(key, value)
      - BatchPrepend(pairs)   (no paper: todos menores que qualquer valor presente)
      - Pull() -> (x, S)      (S com <= M chaves de menor valor, x separa o resto)
    Implementação prática com heapq + best-value por chave (lazy deletion).
    """

    def __init__(self):
        self.M = 1
        self.B = INF
        self.best: Dict[int, float] = {}
        self.heap: List[Tuple[float, int]] = []

    def initialize(self, M: int, B: float):
        self.M = max(1, int(M))
        self.B = B
        self.best.clear()
        self.heap.clear()

    def is_empty(self) -> bool:
        self._cleanup_top()
        return len(self.heap) == 0

    def insert(self, key: int, value: float):
        # Mantém o menor valor por chave
        cur = self.best.get(key, INF)
        if value < cur:
            self.best[key] = value
            heapq.heappush(self.heap, (value, key))

    def batch_prepend(self, pairs: Iterable[Tuple[int, float]]):
        # No paper, esses values são menores que qualquer value já presente.
        # Aqui, a gente só faz "insert" normal; corretude permanece.
        for k, v in pairs:
            self.insert(k, v)

    def pull(self) -> Tuple[float, Set[int]]:
        """
        Retorna:
          - x: bound separador (B se vazio, ou o menor value restante após remover S)
          - S: conjunto com <= M chaves de menor valor
        """
        S: Set[int] = set()
        self._cleanup_top()

        while len(S) < self.M and self.heap:
            val, key = heapq.heappop(self.heap)
            # lazy deletion: ignora se não é mais o melhor
            if self.best.get(key, INF) != val:
                continue
            # remove do "ativo" ao puxar
            del self.best[key]
            S.add(key)

        self._cleanup_top()
        if not self.heap:
            x = self.B
        else:
            x = self.heap[0][0]
        return x, S

    def _cleanup_top(self):
        while self.heap:
            val, key = self.heap[0]
            if self.best.get(key, INF) == val:
                break
            heapq.heappop(self.heap)


def _calc_params(n: int) -> Tuple[int, int, int]:
    """
    Paper usa:
      k = floor(log^{1/3} n)
      t = floor(log^{2/3} n)
      l_top = ceil((log n)/t)
    Assume log base 2 (padrão em análise de algoritmos).
    """
    if n <= 2:
        return 1, 1, 1
    lg = math.log2(n)
    k = max(1, int(lg ** (1.0 / 3.0)))
    t = max(1, int(lg ** (2.0 / 3.0)))
    l_top = max(1, int(math.ceil(lg / t)))
    return k, t, l_top


def _pow2(exp: int) -> int:
    # exp pode ser 0
    if exp <= 0:
        return 1
    return 1 << exp


def base_case(
    B: float,
    S: Set[int],
    adj: List[List[Tuple[int, float]]],
    db: List[float],
    pred: List[PredInfo],
    k: int,
) -> Tuple[float, Set[int]]:
    """
    Algoritmo 2 (BaseCase).
    Requisitos do paper: S={x}, x completo, etc.
    Aqui assumimos S singleton.
    """
    (x,) = tuple(S)
    U0: Set[int] = {x}
    heap: List[Tuple[float, int]] = [(db[x], x)]
    in_heap: Dict[int, float] = {x: db[x]}

    while heap and len(U0) < k + 1:
        du, u = heapq.heappop(heap)
        if in_heap.get(u, INF) != du:
            continue
        del in_heap[u]
        U0.add(u)

        for v, w in adj[u]:
            nd = du + w
            if nd <= db[v] and nd < B:
                db[v] = nd
                pred[v].parent = u
                pred[v].w = w
                # decrease-key lazy
                if nd < in_heap.get(v, INF):
                    in_heap[v] = nd
                    heapq.heappush(heap, (nd, v))

    if len(U0) <= k:
        return B, U0
    else:
        # B' = max_{v in U0} db[v], U = {v in U0 : db[v] < B'}
        Bp = max(db[v] for v in U0)
        U = {v for v in U0 if db[v] < Bp}
        return Bp, U


def find_pivots(
    B: float,
    S: Set[int],
    adj: List[List[Tuple[int, float]]],
    db: List[float],
    pred: List[PredInfo],
    k: int,
) -> Tuple[Set[int], Set[int]]:
    """
    Algoritmo 1 (FindPivots) conforme paper.
    Retorna (P, W).
    """
    W: Set[int] = set(S)
    Wi_prev: Set[int] = set(S)

    for _i in range(1, k + 1):
        Wi: Set[int] = set()
        for u in Wi_prev:
            du = db[u]
            for v, w in adj[u]:
                nd = du + w
                if nd <= db[v]:
                    db[v] = nd
                    pred[v].parent = u
                    pred[v].w = w
                    if nd < B:
                        Wi.add(v)
        W |= Wi
        Wi_prev = Wi

        if len(W) > k * len(S):
            # paper: P <- S e retorna
            return set(S), W

    # Construir F = {(u,v) em E : u,v in W e db[v] = db[u] + wuv}
    # Usamos o pred global: se pred[v] = u e ambos em W e igualdade bate, então (u,v) entra.
    children: Dict[int, List[int]] = {u: [] for u in W}
    indeg: Dict[int, int] = {u: 0 for u in W}

    for v in W:
        u = pred[v].parent
        if u is None:
            continue
        if u in W and v in W:
            # checa igualdade via w armazenado
            if abs(db[v] - (db[u] + pred[v].w)) <= 0.0:
                children.setdefault(u, []).append(v)
                indeg[v] = indeg.get(v, 0) + 1

    # roots do "forest" = nós com indeg 0 dentro de W
    roots = [u for u in W if indeg.get(u, 0) == 0]

    # calcular tamanhos de subárvore
    subtree_size: Dict[int, int] = {}

    def dfs(u: int) -> int:
        s = 1
        for ch in children.get(u, []):
            s += dfs(ch)
        subtree_size[u] = s
        return s

    for r in roots:
        dfs(r)

    P = {u for u in S if subtree_size.get(u, 1) >= k}
    return P, W


def bmssp(
    l: int,
    B: float,
    S: Set[int],
    adj: List[List[Tuple[int, float]]],
    db: List[float],
    pred: List[PredInfo],
    k: int,
    t: int,
) -> Tuple[float, Set[int]]:
    """
    Algoritmo 3 (BMSSP) do paper.
    """
    if l == 0:
        return base_case(B, S, adj, db, pred, k)

    P, W = find_pivots(B, S, adj, db, pred, k)

    D = FrontierDS()
    M = _pow2((l - 1) * t)  # 2^{(l-1)t}
    D.initialize(M, B)

    for x in P:
        D.insert(x, db[x])

    i = 0
    if P:
        Bp_i = min(db[x] for x in P)
    else:
        Bp_i = B
    U: Set[int] = set()

    limit = (k * k) * _pow2(l * t)  # k^2 * 2^{lt}

    while len(U) < limit and (not D.is_empty()):
        i += 1
        Bi, Si = D.pull()  # (B_i, S_i)
        Bp_i, Ui = bmssp(l - 1, Bi, Si, adj, db, pred, k, t)
        U |= Ui

        K_pairs: List[Tuple[int, float]] = []
        for u in Ui:
            du = db[u]
            for v, w in adj[u]:
                nd = du + w
                if nd <= db[v]:
                    db[v] = nd
                    pred[v].parent = u
                    pred[v].w = w
                    if Bi <= nd < B:
                        D.insert(v, nd)
                    elif Bp_i <= nd < Bi:
                        K_pairs.append((v, nd))

        # BatchPrepend(K ∪ {⟨x, db[x]⟩ : x ∈ Si and db[x] ∈ [B′i, Bi)})
        extra = [(x, db[x]) for x in Si if (Bp_i <= db[x] < Bi)]
        D.batch_prepend(K_pairs + extra)

    Bp = min(Bp_i, B)
    U |= {x for x in W if db[x] < Bp}
    return Bp, U


def sssp_break_sorting_barrier(
    adj: List[List[Tuple[int, float]]],
    s: int,
) -> Tuple[List[float], List[Optional[int]]]:
    """
    Executa o algoritmo do paper:
      chama BMSSP com l=ceil((log n)/t), S={s}, B=inf.
    Retorna:
      - distâncias finais (db)
      - predecessor (Pred) para reconstruir caminhos
    """
    n = len(adj)
    k, t, l_top = _calc_params(n)

    db = [INF] * n
    pred = [PredInfo(None, 0.0) for _ in range(n)]
    db[s] = 0.0
    pred[s].parent = None

    # Top level: BMSSP(l_top, inf, {s})
    bmssp(l_top, INF, {s}, adj, db, pred, k, t)

    pred_parent = [p.parent for p in pred]
    return db, pred_parent


# --- Exemplo mínimo de uso ---
if __name__ == "__main__":
    # grafo dirigido: 0->1 (1), 0->2 (4), 1->2 (2), 1->3 (6), 2->3 (3)
    adj_list = [
        [(1, 4), (2, 2)],          # Vizinhos do 0 (1)
        [(2, 3), (3, 2), (4, 3)],  # Vizinhos do 1 (2)
        [(1, 1), (3, 4), (4, 5)],  # Vizinhos do 2 (3)
        [],                        # Vizinhos do 3 (4) - Sem saída
        [(3, 1)]                   # Vizinhos do 4 (5)
    ]
    dist, pred = sssp_break_sorting_barrier(adj_list, 0)
    print("dist:", dist)
    print("pred:", pred)
