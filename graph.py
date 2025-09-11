import networkx as nx
import random
from matplotlib import pyplot as plt

def grafo_debug():
    G = nx.DiGraph() #creare il grafo diretto

    # Aggiungere archi con pesi
    edges = [
        ('s', '2', 3), 
        ('s', '3', 3), 
        ('s', '4', 2), 
        ('2', '5', 4), 
        ('4', '2', 1), 
        ('4', 't', 2), 
        ('5', 't', 1), 
        ('5', '4', 1), 
        ('3', '4', 1), 
        ('3', 't', 2)
    ]

    for u, v, w in edges:
        G.add_edge(u, v, capacity=w)

    return G

def create_directed_flow_graph(n, max_u, edge_prob=0.2):
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    s = 0
    t = n - 1

    # Aggiungi archi casuali con probabilità 'edge_prob'
    for i in range(n):
        for j in range(n):
            if i != t and j != s and i != j and random.random() < edge_prob:
                if not G.has_edge(j, i):
                    G.add_edge(i, j)

    # Aggiungi un percorso forzato da 's' a 't' se non esiste
    if not nx.has_path(G, s, t):
        # Aggiungi un percorso lineare da 's' a 't'
        for i in range(n - 1):
            if not G.has_edge(i, i + 1):
                G.add_edge(i, i + 1)

    # Aggiungi capacità casuali agli archi
    for u, v in G.edges():
        G[u][v]['capacity'] = random.randint(1, max_u)

    # Controllo avanzato di connettività tramite min-cut
    min_cut_value, (reachable, non_reachable) = nx.minimum_cut(G, s, t)

    # Se il min-cut è troppo basso, rigenera il grafo con un edge_prob più alto
    if min_cut_value < max_u / 2:
        return create_directed_flow_graph(n, max_u, edge_prob + 0.1)
    
    for u, v in G.edges():
        if G.has_edge(v, u):
            G.remove_edge(v, u)

    return G, s, t

def create_residual_graph(G, x):
    R = nx.DiGraph()  # Initialize the residual graph
    for u, v in G.edges():
        # Forward residual capacity (remaining capacity)
        forward_residual = G[u][v]['capacity'] - x[(u, v)]
        if forward_residual >= 0:
            R.add_edge(u, v, residual=forward_residual, capacity=G[u][v]['capacity'])
        
        # Backward residual capacity (ability to return flow)
        if x[(u, v)] >= 0:
            R.add_edge(v, u, residual=x[(u, v)],capacity = 0)
    
    return R


def plot_residual_graph(R):
    fig = plt.figure(2, figsize=(8, 8))
    fig.suptitle("Grafo Residuo")

    # Ottieni le posizioni dei nodi (layout) per plottare il grafo
    pos = nx.spring_layout(R)

    # Disegna i nodi
    nx.draw_networkx_nodes(R, pos, node_size=500, node_color='lightblue')

    # Disegna le etichette dei nodi
    nx.draw_networkx_labels(R, pos)

    # Disegna gli archi diretti con frecce
    directed_edges = []
    reverse_edges = []

    # Separiamo gli archi diretti e inversi
    for u, v in R.edges():
        if R.has_edge(v, u):  # Se esiste anche l'arco inverso
            reverse_edges.append((u, v))
        else:
            directed_edges.append((u, v))

    # Disegna gli archi diretti (i,j)
    nx.draw_networkx_edges(R, pos, edgelist=directed_edges, arrowstyle='->', arrowsize=20, edge_color='blue', connectionstyle='arc3,rad=0.1')

    # Disegna gli archi inversi (j,i) con una leggera curva inversa
    nx.draw_networkx_edges(R, pos, edgelist=reverse_edges, arrowstyle='->', arrowsize=20, edge_color='red', connectionstyle='arc3,rad=-0.1')

    # Disegna le etichette delle capacità per ogni arco
    edge_labels = {}
    for u, v in R.edges():
        residual_capacity = R[u][v]['residual']
        edge_labels[(u, v)] = f"{residual_capacity}"

    # Assicurati che entrambe le etichette per (u,v) e (v,u) vengano mostrate
    nx.draw_networkx_edge_labels(R, pos, edge_labels=edge_labels)

    # Mostra il grafico
    plt.axis('off')  # Nascondi gli assi
    plt.show()