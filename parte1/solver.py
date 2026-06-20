import heapq

def carregar(arq):
    with open(arq, 'r', encoding='utf-8') as f:
        d = [l.strip().split('\t') for l in f if l.strip()]
    
    n_v, n_a = map(int, d[0])
    s, t = map(int, d[1])
    
    arest = []
    neg = False
    for i in range(2, len(d)):
        u, v, w = int(d[i][0]), int(d[i][1]), float(d[i][2])
        if w.is_integer(): w = int(w)
        arest.append((u, v, w))
        if w < 0: neg = True
            
    return n_v, s, t, arest, neg

def dijkstra(n, s, t, arest):
    adj = {i: [] for i in range(n)}
    for u, v, w in arest: adj[u].append((v, w))
        
    dist = {i: float('inf') for i in range(n)}
    ant = {i: None for i in range(n)}
    dist[s] = 0
    pq = [(0, s)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                ant[v] = u
                heapq.heappush(pq, (dist[v], v))
                
    path = []
    curr = t
    while curr is not None:
        path.append(curr)
        curr = ant[curr]
    return path[::-1], dist[t]

def bellman(n, s, t, arest):
    dist = {i: float('inf') for i in range(n)}
    ant = {i: None for i in range(n)}
    dist[s] = 0
    
    for _ in range(n - 1):
        for u, v, w in arest:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                ant[v] = u
    
    path = []
    curr = t
    while curr is not None:
        path.append(curr)
        curr = ant[curr]
    return path[::-1], dist[t]

def rodar(in_f, out_f):
    n, s, t, arest, neg = carregar(in_f)
    if neg:
        alg, just = "Bellman-Ford", "O algoritmo de Dijkstra não é aplicável a grafos com pesos negativos. Bellman-Ford é utilizado aqui pela capacidade de tratar custos negativos (SLA) via relaxamento iterativo."
        path, val = bellman(n, s, t, arest)
    else:
        alg, just = "Dijkstra", "Dijkstra é o método de caminho mínimo mais eficiente para grafos sem circuitos de custo negativo, utilizando uma estratégia gulosa com complexidade ótima."
        path, val = dijkstra(n, s, t, arest)
        
    with open(out_f, 'w') as f:
        f.write(f"ALGORITMO: {alg}\nJUSTIFICATIVA: {just}\nROTA: {' '.join(map(str, path))}\nCUSTO: {val}\n")

if __name__ == "__main__":
    rodar("grafo_rede_p.txt", "saida_parte1_p.txt")
    rodar("grafo_rede_m.txt", "saida_parte1_m.txt")