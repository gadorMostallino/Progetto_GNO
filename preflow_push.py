
import networkx as nx
import math


def generic_preflow_push(R,s,t,max_iterations = 100000):
    def preproc():
        #calcolo le distanze esatte da ogni nodo a t come il numero minimo di archi tra i e t
        for u in R:
            if  nx.has_path(R,u,t):
                d[u] = nx.shortest_path_length(R,u,t)
            else:
                d[u] = float('inf')
        
        #push iniziale del flusso dalla sorgente
        for v in R[s]:
            ''' flow[(s,v)] = G[s][v]['capacity']
            e[v] = G[s][v]['capacity']
            e[s] -= G[s][v]['capacity']'''
            delta = R[s][v]['capacity']
            push(s,v,delta)
            
            
        d[s] = len(R)

    def push(u,v,delta):
        R[u][v]['residual'] -= delta
        R[v][u]['residual'] += delta
        e[u] -= delta
        e[v] += delta
        if e[v] > 0 and v != t and v != s:
            if v not in active_nodes:
                active_nodes.append(v)
        if e[u] > 0 and u != t and u != s:
            if v not in active_nodes:
                active_nodes.append(v)


    def relabel(u):
        min_height = float('inf')
        for v in R[u]:
            if R[u][v]['residual'] > 0:
                min_height = min(min_height,d[v])
        d[u] = min_height + 1

    def push_relabel(u):
        pushed = False
        for v in R[u]:
            r_uv = R[u][v]['residual']
            if d[u] == d[v] + 1 and r_uv > 0:
                pushed = True # controllo se l'arco è ammissibile
                delta = min(e[u],r_uv)
                push(u,v,delta)
                break
        
        relabel(u)
                



    active_nodes = []
    d = {}
    e = {u:0 for u in R}
    iteraction = 0

    preproc()

    while active_nodes:
        iteraction += 1
        u = active_nodes.pop(0)
        push_relabel(u)

        #DEBUG
        active_nodes.clear()
        for u in R:
            if e[u] > 0 and u != t and u != s:
                active_nodes.append(u)

        if iteraction == max_iterations:
            break
    if iteraction >= max_iterations:
        print("loop infinito")
        return None
    else:
        flow = {}
        for u in R:
            for v in R[u]:
                if R[u][v]['capacity'] > 0:
                    flow[(u,v)] = R[v][u]['residual']
        max_flow = sum([flow[(s,v)] for v in R[s]])
        return max_flow,flow
    
def highest_lable_preflow_push(R,s,t,max_iterations = 100000):
    def preproc():
        #calcolo le distanze esatte da ogni nodo a t come il numero minimo di archi tra i e t
        for u in R:
            if  nx.has_path(R,u,t):
                d[u] = nx.shortest_path_length(R,u,t)
            else:
                d[u] = float('inf')
        
        #push iniziale del flusso dalla sorgente
        for v in R[s]:
            ''' flow[(s,v)] = G[s][v]['capacity']
            e[v] = G[s][v]['capacity']
            e[s] -= G[s][v]['capacity']'''
            delta = R[s][v]['capacity']
            push(s,v,delta)
            
            
        d[s] = len(R)

    def push(u,v,delta):
        R[u][v]['residual'] -= delta 
        R[v][u]['residual'] += delta 
        e[u] -= delta
        e[v] += delta
        if e[v] > 0 and v != t and v != s:
            if v not in active_nodes:
                active_nodes.append(v)
        if e[u] > 0 and u != t and u != s:
            if u not in active_nodes:
                active_nodes.append(v)


    def relabel(u):
        min_height = float('inf')
        for v in R[u]:
            if R[u][v]['residual'] > 0:
                min_height = min(min_height,d[v])
        d[u] = min_height + 1

    def push_relabel(u):
        pushed = False
        for v in R[u]:
            r_uv = R[u][v]['residual']
            if d[u] == d[v] + 1 and r_uv > 0:
                pushed = True # controllo se l'arco è ammissibile
                delta = min(e[u],r_uv)
                push(u,v,delta)
                break
        
        relabel(u)
                



    active_nodes = []
    d = {}
    e = {u:0 for u in R}
    iteraction = 0

    preproc()

    while active_nodes:
        iteraction += 1

        #sort dei nodi attivi in base alla distance label
        active_nodes.sort(key = lambda x: d[x],reverse = True) 

        u = active_nodes.pop(0)
        push_relabel(u)

        if iteraction == max_iterations:
            break
    if iteraction >= max_iterations:
        print("loop infinito")
        return None
    else:

        flow = {}
        for u in R:
            for v in R[u]:
                if R[u][v]['capacity'] > 0:
                    flow[(u,v)] = R[v][u]['residual']
        max_flow = sum([flow[(s,v)] for v in R[s]])
        return max_flow,flow
    

def excess_scaling_preflow_push(R, s, t, max_iterations=100000):
    def preproc():
        #calcolo le distanze esatte da ogni nodo a t come il numero minimo di archi tra i e t
        for u in R:
            if  nx.has_path(R,u,t):
                d[u] = nx.shortest_path_length(R,u,t)
            else:
                d[u] = float('inf')
        
        #push iniziale del flusso dalla sorgente
        for v in R[s]:
            ''' flow[(s,v)] = G[s][v]['capacity']
            e[v] = G[s][v]['capacity']
            e[s] -= G[s][v]['capacity']'''
            delta = R[s][v]['capacity']
            push(s,v,delta)
            
            
        d[s] = len(R)

    def push(u, v, delta):
        R[u][v]['residual'] -= delta
        R[v][u]['residual'] += delta
        e[u] -= delta
        e[v] += delta
        # attiva il nodo v se ha eccesso sufficiente
        if e[v] >= Delta and v not in {s, t}:
            active_nodes.append(v)
        # anche u può rimanere attivo
        if e[u] >= Delta and u not in {s, t}:
            active_nodes.append(u)

    def relabel(u):
        min_height = float('inf')
        for v in R[u]:
            if R[u][v]['residual'] > 0:
                min_height = min(min_height, d[v])
        d[u] = min_height + 1

    def push_relabel(u):
        while e[u] >= Delta:
            pushed = False
            for v in R[u]:
                r_uv = R[u][v]['residual']
                if d[u] == d[v] + 1 and r_uv > 0:
                    delta = min(e[u], r_uv)
                    push(u, v, delta)
                    pushed = True
                    if e[u] < Delta:
                        break
            if not pushed:  # nessun arco ammissibile → relabel
                relabel(u)

    # Inizializzazione
    active_nodes = []
    d = {}
    e = {u: 0 for u in R}
    iteration = 0

    # Delta iniziale
    max_cap = max(R[u][v]['capacity'] for u in R for v in R[u] if 'capacity' in R[u][v])
    Delta = 2 ** int(math.floor(math.log2(max_cap)))

    preproc()


    while Delta >= 1:
        # costruisci lista dei nodi attivi per questo Delta
        active_nodes = [u for u in R if e[u] >= Delta and u not in {s, t}]

        while active_nodes:
            iteration += 1
            if iteration >= max_iterations:
                print("loop infinito")
                return None

            active_nodes.sort(key=lambda x: d[x], reverse=False) #ordino in base alla distance label minore
            u = active_nodes.pop(0)  # prende un nodo arbitrario dal set
            push_relabel(u)

        Delta //= 2  # dimezza la soglia

    # Ricostruzione del flusso
    flow = {}
    for u in R:
        for v in R[u]:
            if R[u][v]['capacity'] > 0:
                flow[(u, v)] = R[v][u]['residual']
    max_flow = sum(flow[(s, v)] for v in R[s])
    return max_flow, flow
