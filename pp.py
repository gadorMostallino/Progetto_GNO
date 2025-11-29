import pp as pp 
import networkx as nx
import math

from collections import deque


#vecchi algoritmi (problematici)
def generic_preflow_push(R,s,t,max_iterations = 10000000):
    """
    Calcola il flusso massimo in un grafo G dalla sorgente s al pozzo t
    usando una versione ottimizzata dell'algoritmo Preflow-Push.
    
    Args:
        G (nx.DiGraph): Il grafo di input con attributo 'capacity' sugli archi.
        s: Il nodo sorgente.
        t: Il nodo pozzo.

    Returns:
        tuple: Una tupla contenente il valore del flusso massimo e un dizionario
               che rappresenta il flusso su ogni arco.
    """
    
    # Inizializza i dizionari per eccesso (e) e altezza (d)
    e = {node: 0 for node in R.nodes()}
    d = {node: 0 for node in R.nodes()}
    
    # Crea un grafo residuo con capacità iniziali
    #R = nx.DiGraph()
    for u, v, data in R.edges(data=True):
        R.add_edge(u, v, capacity=data['capacity'], residual=data['capacity'])
        R.add_edge(v, u, capacity=0, residual=0)

    # Usa una BFS inversa per calcolare le altezze iniziali da t
    queue = deque([t])
    visited = {t}
    d[t] = 0
    while queue:
        u = queue.popleft()
        for v in R.predecessors(u):
            if v not in visited:
                d[v] = d[u] + 1
                visited.add(v)
                queue.append(v)
    
    # L'altezza della sorgente (s) viene impostata a N per convenzione
    d[s] = len(R.nodes)

    # Spinge il flusso iniziale dalla sorgente
    for v in R.neighbors(s):
        delta = R.edges[s, v]['capacity']
        R.edges[s, v]['residual'] -= delta
        R.edges[v, s]['residual'] += delta
        e[v] += delta
        e[s] -= delta

    # Usa una deque per gestire i nodi attivi in modo efficiente (FIFO)
    active_nodes_queue = deque([u for u in R.nodes() if e[u] > 0 and u != s and u != t])
    
    while active_nodes_queue:
        u = active_nodes_queue.popleft()
        
        while e[u] > 0:
            pushed = False
            for v in R.neighbors(u):
                if d[u] == d[v] + 1 and R.edges[u, v]['residual'] > 0:
                    delta = min(e[u], R.edges[u, v]['residual'])
                    
                    R.edges[u, v]['residual'] -= delta
                    R.edges[v, u]['residual'] += delta
                    e[u] -= delta
                    e[v] += delta
                    pushed = True
                    
                    if e[v] > 0 and v != s and v != t and v not in active_nodes_queue:
                        active_nodes_queue.append(v)
                    
                    if e[u] == 0:
                        break
            
            if not pushed:
                min_height = float('inf')
                for v in R.neighbors(u):
                    if R.edges[u, v]['residual'] > 0:
                        min_height = min(min_height, d[v])
                d[u] = min_height + 1
                
                if e[u] > 0 and u != s and u != t:
                     active_nodes_queue.append(u)

    # Calcola il flusso finale e il flusso massimo
    flow = {}
    for u, v, data in R.edges(data=True):
        # Il flusso su un arco (u, v) è la capacità iniziale meno la capacità residua
        flow[(u, v)] = data['capacity'] - R.edges[u, v]['residual']

    max_flow = sum(flow[(s, v)] for v in R.neighbors(s))
    
    return max_flow, flow

def highest_label_preflow_pushg(R,s,t,max_iterations = 10000000):
    """
    Calcola il flusso massimo in un grafo G dalla sorgente s al pozzo t
    usando una versione ottimizzata dell'algoritmo Preflow-Push.
    
    Args:
        G (nx.DiGraph): Il grafo di input con attributo 'capacity' sugli archi.
        s: Il nodo sorgente.
        t: Il nodo pozzo.
    Returns:
        tuple: Una tupla contenente il valore del flusso massimo e un dizionario
               che rappresenta il flusso su ogni arco.
    """
    
    # Inizializza i dizionari per eccesso (e) e altezza (d)
    e = {node: 0 for node in R.nodes()}
    d = {node: 0 for node in R.nodes()}
    
    # Crea un grafo residuo con capacità iniziali
    #R = nx.DiGraph()
    for u, v, data in R.edges(data=True):
        R.add_edge(u, v, capacity=data['capacity'], residual=data['capacity'])
        R.add_edge(v, u, capacity=0, residual=0)

    # Usa una BFS inversa per calcolare le altezze iniziali da t
    queue = deque([t])
    visited = {t}
    d[t] = 0
    while queue:
        u = queue.popleft()
        for v in R.predecessors(u):
            if v not in visited:
                d[v] = d[u] + 1
                visited.add(v)
                queue.append(v)
    
    # L'altezza della sorgente (s) viene impostata a N per convenzione
    d[s] = len(R.nodes)

    # PUSH: Spinge il flusso iniziale dalla sorgente
    for v in R.neighbors(s):
        delta = R.edges[s, v]['capacity']
        R.edges[s, v]['residual'] -= delta
        R.edges[v, s]['residual'] += delta
        e[v] += delta
        e[s] -= delta

    # Usa una deque per gestire i nodi attivi in modo efficiente (FIFO)
    active_nodes_queue = deque([u for u in R.nodes() if e[u] > 0 and u != s and u != t])
    
    while active_nodes_queue:
        active_nodes_queue = deque(sorted(active_nodes_queue, key=lambda x: d[x], reverse=True))
        u = active_nodes_queue.popleft()
        
        while e[u] > 0:
            pushed = False
            for v in R.neighbors(u):
                if d[u] == d[v] + 1 and R.edges[u, v]['residual'] > 0:
                    delta = min(e[u], R.edges[u, v]['residual'])
                    
                    R.edges[u, v]['residual'] -= delta
                    R.edges[v, u]['residual'] += delta
                    e[u] -= delta
                    e[v] += delta
                    pushed = True
                    
                    if e[v] > 0 and v != s and v != t and v not in active_nodes_queue:
                        active_nodes_queue.append(v)
                    
                    if e[u] == 0:
                        break
            
            if not pushed:
                min_height = float('inf')
                for v in R.neighbors(u):
                    if R.edges[u, v]['residual'] > 0:
                        min_height = min(min_height, d[v])
                d[u] = min_height + 1
                
                if e[u] > 0 and u != s and u != t:
                     active_nodes_queue.append(u)

    # Calcola il flusso finale e il flusso massimo
    flow = {}
    for u, v, data in R.edges(data=True):
        # Il flusso su un arco (u, v) è la capacità iniziale meno la capacità residua
        flow[(u, v)] = data['capacity'] - R.edges[u, v]['residual']

    max_flow = sum(flow[(s, v)] for v in R.neighbors(s))
    
    return max_flow, flow

def excess_scaling_preflow_pushh(R, s, t, max_iterations=10000000):
    ''' 
    Calcola il flusso massimo in un grafo G dalla sorgente s al pozzo t
    usando l'algoritmo Preflow-Push con scaling dell'eccesso.
    Args:
        G (nx.DiGraph): Il grafo di input con attributo 'capacity' sugli archi.
        s: Il nodo sorgente.
        t: Il nodo pozzo.
    Returns:
        tuple: Una tupla contenente il valore del flusso massimo e un dizionario
               che rappresenta il flusso su ogni arco.
    '''
    # Inizializza i dizionari per eccesso (e) e altezza (d)
    e = {node: 0 for node in R.nodes()}
    d = {node: 0 for node in R.nodes()}
    
    # Crea un grafo residuo con capacità iniziali
    for u, v, data in R.edges(data=True):
        R.add_edge(u, v, capacity=data['capacity'], residual=data['capacity'])
        R.add_edge(v, u, capacity=0, residual=0)
    # Usa una BFS inversa per calcolare le altezze iniziali da t
    queue = deque([t])
    visited = {t}  
    d[t] = 0
    while queue:
        u = queue.popleft()
        for v in R.predecessors(u):
            if v not in visited:
                d[v] = d[u] + 1
                visited.add(v)
                queue.append(v)
    # L'altezza della sorgente (s) viene impostata a N per convenzione
    d[s] = len(R.nodes)
    
    # PUSH: Spinge il flusso iniziale dalla sorgente
    for v in R.neighbors(s):
        delta = R.edges[s, v]['capacity']
        R.edges[s, v]['residual'] -= delta
        R.edges[v, s]['residual'] += delta
        e[v] += delta
        e[s] -= delta
    # Trova la capacità massima nel grafo per inizializzare il parametro di scaling
    U = max(data['capacity'] for u, v, data in R.edges(data=True))
    # Inizializza il parametro di scaling
    delta = 2 ** (U.bit_length() - 1)
    
    while delta >= 1:
        # Usa una deque per gestire i nodi attivi con eccesso >= delta
        active_nodes_queue = deque([u for u in R.nodes() if e[u] >= delta and u != s and u != t])
        
        while active_nodes_queue:
            u = active_nodes_queue.popleft()
            
            while e[u] >= delta:
                pushed = False
                for v in R.neighbors(u):
                    if d[u] == d[v] + 1 and R.edges[u, v]['residual'] > 0:
                        push_amount = min(e[u], R.edges[u, v]['residual'])
                        if push_amount >= delta:
                            R.edges[u, v]['residual'] -= push_amount
                            R.edges[v, u]['residual'] += push_amount
                            e[u] -= push_amount
                            e[v] += push_amount
                            pushed = True
                            
                            if e[v] >= delta and v != s and v != t and v not in active_nodes_queue:
                                active_nodes_queue.append(v)
                            
                            if e[u] < delta:
                                break
                
                if not pushed:
                    min_height = float('inf')
                    for v in R.neighbors(u):
                        if R.edges[u, v]['residual'] > 0:
                            min_height = min(min_height, d[v])
                    d[u] = min_height + 1
                    
                    if e[u] >= delta and u != s and u != t:
                         active_nodes_queue.append(u)
        # Riduci il parametro di scaling
        delta //= 2
        
    # Calcola il flusso finale e il flusso massimo
    flow = {}
    for u, v, data in R.edges(data=True):
        # Il flusso su un arco (u, v) è la capacità iniziale meno la capacità residua
        flow[(u, v)] = data['capacity'] - R.edges[u, v]['residual']
    max_flow = sum(flow[(s, v)] for v in R.neighbors(s))
    return max_flow, flow



# dovrebbero essere corretti

def FIFO_preflow_push_new(R, s, t, max_iterations=10000000):
    original_edges = list(R.edges(data=True))
    for u, v, data in original_edges:
        R[u][v]['residual'] = data['capacity']

        # Gestione dell'arco inverso (v, u)
        if not R.has_edge(v, u):
            # Se non esiste, lo creiamo con capacità 0 (serve solo per spingere indietro il flusso)
            R.add_edge(v, u, capacity=0, residual=0)
        else:
            # Se esiste già (es. grafo bidirezionale), ci assicuriamo che abbia l'attributo residual
            if 'residual' not in R[v][u]:
                R[v][u]['residual'] = 0

    e = {node: 0 for node in R.nodes()}
    d = {node: 0 for node in R.nodes()}
    
    active_queue = deque()   
    # Verifica se un nodo è gia in coda  
    in_queue = set()    

    def initialize_heights():
        "Esegue una BFS inversa partendo da t per calcolare le distanze esatte iniziali."

        queue = deque([t])
        visited = {t}
        d[t] = 0

        # Inizializza gli altri nodi a un valore "infinito" pratico (N + 1)
        for n in R.nodes():
            if n != t: 
                d[n] = len(R) + 1
            
        while queue:
            u = queue.popleft()
            for v in R.predecessors(u):
                if v not in visited:
                    visited.add(v)
                    d[v] = d[u] + 1
                    queue.append(v)

        # Per definizione, l'altezza della sorgente è pari al numero di nodi N
        d[s] = len(R)

    def push(u, v, delta):
        """Spinge 'delta' flusso da u a v."""

        # Aggiorna le capacità residue
        R[u][v]['residual'] -= delta
        R[v][u]['residual'] += delta

        # Aggiorna gli eccessi
        e[u] -= delta
        e[v] += delta
        
        # Se v diventa attivo (ha eccesso) e non è sorgente/pozzo, va messo in coda
        if e[v] > 0 and v != s and v != t:
            if v not in in_queue:
                active_queue.append(v)
                in_queue.add(v)

    def relabel(u):
        """
        Aumenta l'altezza di u quanto basta per permettere un push verso il vicino
        più basso ammissibile.
        """

        min_height = float('inf')
        possible_move = False

        # Cerca il vicino con altezza minima tra quelli verso cui c'è capacità residua
        for v in R.neighbors(u):
            if R[u][v]['residual'] > 0:
                min_height = min(min_height, d[v])
                possible_move = True
        
        if possible_move:
            d[u] = min_height + 1 # La nuova altezza deve essere 1 in più del vicino più basso
        else:
            d[u] += 1 # Se non ci sono vicini residui (nodo isolato nel residuo)

    def discharge(u):
        """
        Continua a eseguire push e relabel su u finché il suo eccesso non diventa 0
        o non è stato completamente processato.
        """

        while e[u] > 0:
            pushed = False
            neighbors = list(R.neighbors(u))
            for v in neighbors:
                # Condizione di ammissibilità: capacità disponibile e discesa (d[u] == d[v] + 1)
                if R[u][v]['residual'] > 0 and d[u] == d[v] + 1:
                    delta = min(e[u], R[u][v]['residual'])
                    push(u, v, delta)
                    pushed = True
                    # Se l'eccesso è esaurito
                    if e[u] == 0:
                        break

            # Se non è stato possibile spingere flusso da nessuna parte, dobbiamo alzare u
            if not pushed:
                relabel(u)

    initialize_heights()

    # Preflow iniziale: satura tutti gli archi uscenti da s
    for v in R.neighbors(s):
        delta = R[s][v]['residual']
        if delta > 0:
            R[s][v]['residual'] -= delta
            R[v][s]['residual'] += delta
            e[v] += delta
            e[s] -= delta
            
            # Aggiunge i vicini di s alla coda se non sono t
            if v != t and v != s and v not in in_queue:
                active_queue.append(v)
                in_queue.add(v)

    iteration = 0
    while active_queue:
        iteration += 1
        if iteration > max_iterations:
            return 0, {} # Per evitare loop infiniti

        # Preleva il prossimo nodo attivo (FIFO)
        u = active_queue.popleft()
        in_queue.remove(u) # Rimuove dal set di tracciamento
        
        discharge(u)
        
        # Se dopo il discharge il nodo ha ancora eccesso (è stato relabeled ma non svuotato),
        # deve tornare in coda per essere processato nuovamente.
        if e[u] > 0 and u != s and u != t:
            if u not in in_queue:
                active_queue.append(u)
                in_queue.add(u)

    flow = {}
    for u, v, data in R.edges(data=True):
        original_cap = data.get('capacity', 0)
        # Il flusso effettivo è ( capacità originale - residuo finale )
        if original_cap > 0:
            flow[(u, v)] = original_cap - R[u][v]['residual']

    # Flusso totale uscente dalla sorgente
    max_flow = sum(flow.get((s, v), 0) for v in R.neighbors(s))

    return max_flow, flow

def excess_scaling_preflow_push_new(R, s, t, max_iterations=10000000):

    # Ci assicuriamo che esistano gli archi inversi per ogni arco diretto
    # Nota: Usiamo list() per creare una copia statica degli archi prima di aggiungerne di nuovi
    original_edges = list(R.edges(data=True))

    for u, v, data in original_edges:
        # Inizializza residuale sull'arco diretto
        R[u][v]['residual'] = data['capacity']

        # Se non esiste l'arco inverso, crealo con capacità 0
        if not R.has_edge(v, u):
            R.add_edge(v, u, capacity=0, residual=0)
        else:
            # Se esiste già (es. grafo bidirezionale), assicurati che il residuale sia inizializzato
            if 'residual' not in R[v][u]:
                R[v][u]['residual'] = 0

    e = {node: 0 for node in R.nodes()}
    d = {node: 0 for node in R.nodes()}
    
    # BFS Inversa per le altezze iniziali (distanza esatta da t)
    queue = deque([t])
    visited = {t}
    d[t] = 0

    while queue:
        u = queue.popleft()
        for v in R.predecessors(u):
            # Consideriamo solo archi che possono portare flusso verso t (nel residuo v->u ha cap > 0)
            # Tuttavia, per l'inizializzazione delle distanze geometriche, seguiamo la topologia inversa
            if v not in visited:
                d[v] = d[u] + 1
                visited.add(v)
                queue.append(v)
    
    d[s] = len(R.nodes()) # Altezza sorgente = N

    # Push Iniziale dalla sorgente
    for v in R.neighbors(s):
        delta_push = R[s][v]['residual']
        if delta_push > 0:
            R[s][v]['residual'] -= delta_push
            R[v][s]['residual'] += delta_push
            e[v] += delta_push
            e[s] -= delta_push

    # Calcolo Delta Iniziale (Scaling Parameter)
    # Trova la capacità massima tra gli archi originali
    max_cap = 0
    for u, v, data in R.edges(data=True):
        max_cap = max(max_cap, data.get('capacity', 0))
    
    if max_cap == 0:
        return 0, {}

    # Delta parte dalla potenza di 2 più vicina a max_cap
    delta = 2 ** (max_cap.bit_length())

    # Loop Principale di Scaling
    while delta >= 1:
        # Identifica nodi con eccesso elevato (> delta)
        active_nodes_queue = deque([u for u in R.nodes() if e[u] >= delta and u != s and u != t])
        in_queue = {u for u in active_nodes_queue} # Set per lookup O(1)

        while active_nodes_queue:
            u = active_nodes_queue.popleft()
            in_queue.remove(u)

            # Esegui DISCHARGE sul nodo u finché ha troppo eccesso
            while e[u] >= delta:
                pushed = False
                
                # Tentativo di Push verso i vicini
                neighbors = list(R.neighbors(u)) # Lista statica per sicurezza
                
                # Ottimizzazione: ordina i vicini per altezza (ottimizzazione facoltativa)
                neighbors.sort(key=lambda x: d[x]) 
                
                for v in neighbors:
                    # Condizione di ammissibilità: altezza corretta e spazio residuo
                    if d[u] == d[v] + 1 and R[u][v]['residual'] > 0:
                        
                        # Quanto possiamo spingere? 
                        # Nello scaling non siamo obbligati a spingere 'delta', 
                        # basta spingere quello che si può per ridurre l'eccesso.
                        push_amount = min(e[u], R[u][v]['residual'])
                        
                        if push_amount > 0:
                            R[u][v]['residual'] -= push_amount
                            R[v][u]['residual'] += push_amount
                            e[u] -= push_amount
                            e[v] += push_amount
                            pushed = True
                            
                            # Gestione nodo ricevente v
                            # Se v ora ha abbastanza eccesso e non è sorgente/pozzo, mettilo in coda
                            if e[v] >= delta and v != s and v != t:
                                if v not in in_queue:
                                    active_nodes_queue.append(v)
                                    in_queue.add(v)
                            
                            # Se l'eccesso di u scende sotto delta, smettiamo di processarlo per questa fase
                            if e[u] < delta:
                                break
                
                # Se non abbiamo spinto nulla ma abbiamo ancora eccesso >= delta, dobbiamo fare Relabel
                if not pushed:
                    min_height = float('inf')
                    possible_move = False
                    for v in R.neighbors(u):
                        if R[u][v]['residual'] > 0:
                            min_height = min(min_height, d[v])
                            possible_move = True
                    
                    if possible_move:
                        d[u] = min_height + 1
                    else:
                        # Se il nodo è isolato nel residuo (non può mandare nulla), alza l'altezza per sbloccarlo
                        d[u] += 1
                        
        # Riduciamo il parametro di scaling
        delta //= 2

    # Calcolo Risultato Finale
    flow = {}
    for u, v, data in R.edges(data=True):
        # Il flusso è (capacità originale - residuo)
        # Attenzione: consideriamo solo gli archi che avevano capacità originale > 0
        original_cap = data.get('capacity', 0)
        if original_cap > 0:
            flow[(u, v)] = original_cap - R[u][v]['residual']
    
    max_flow = sum(flow.get((s, v), 0) for v in R.neighbors(s))
    
    return max_flow, flow

def highest_label_preflow_push_new(R, s, t, max_iterations=10000000):
    
    original_edges = list(R.edges(data=True))
    for u, v, data in original_edges:
        R[u][v]['residual'] = data['capacity']
        # Crea arco inverso se non esiste
        if not R.has_edge(v, u):
            R.add_edge(v, u, capacity=0, residual=0)
        else:
            if 'residual' not in R[v][u]:
                R[v][u]['residual'] = 0

    e = {node: 0 for node in R.nodes()} # Excess
    d = {node: 0 for node in R.nodes()} # Height/Label
    
    active_nodes = []     
    active_set = set()    

    def initialize_heights():
        # BFS Inversa da t
        queue = deque([t])
        visited = {t}
        d[t] = 0
        # Inizializza tutti gli altri a infinito
        for n in R.nodes():
            if n != t: d[n] = len(R) + 1 
            
        while queue:
            u = queue.popleft()
            for v in R.predecessors(u):
                # Se c'è capacità nel grafo residuo (v->u ha capacità > 0 nel grafo originale/inverso)
                # Qui semplifichiamo controllando solo se non visitato, assumendo il grafo connesso
                if v not in visited:
                    visited.add(v)
                    d[v] = d[u] + 1
                    queue.append(v)
        d[s] = len(R)

    def push(u, v, delta):
        R[u][v]['residual'] -= delta
        R[v][u]['residual'] += delta
        e[u] -= delta
        e[v] += delta
        
        # Aggiungi v ai nodi attivi se ha eccesso e non è s o t
        if e[v] > 0 and v != s and v != t:
            if v not in active_set:
                active_nodes.append(v)
                active_set.add(v)

    def relabel(u):
        min_height = float('inf')
        possible_move = False
        for v in R.neighbors(u):
            if R[u][v]['residual'] > 0:
                min_height = min(min_height, d[v])
                possible_move = True
        
        if possible_move:
            d[u] = min_height + 1
        else:
            # Se il nodo è bloccato, alza l'altezza per sbloccarlo
            d[u] += 1

    def discharge(u):
        while e[u] > 0:
            pushed = False
            neighbors = list(R.neighbors(u))
            for v in neighbors:
                # Condizione di ammissibilità: altezza esatta e spazio residuo
                if R[u][v]['residual'] > 0 and d[u] == d[v] + 1:
                    delta = min(e[u], R[u][v]['residual'])
                    push(u, v, delta)
                    pushed = True
                    if e[u] == 0:
                        break
            
            if not pushed:
                relabel(u)
                # Se dopo il relabel ha ancora eccesso, il while continua

    initialize_heights()

    # Push Iniziale dalla sorgente
    for v in R.neighbors(s):
        delta = R[s][v]['residual']
        if delta > 0:
            R[s][v]['residual'] -= delta
            R[v][s]['residual'] += delta
            e[v] += delta
            e[s] -= delta
            
            if v != t and v != s and v not in active_set:
                active_nodes.append(v)
                active_set.add(v)

    iteration = 0
    while active_nodes:
        iteration += 1
        if iteration > max_iterations:
            print("Loop infinito o limite iterazioni raggiunto")
            return 0, {}

        # Highest Label selection
        active_nodes.sort(key=lambda x: d[x], reverse=True)
        u = active_nodes.pop(0)
        active_set.remove(u)
        
        discharge(u)
        
        # Se dopo il discharge u ha ancora eccesso (es. relabel lo ha alzato ma non ha svuotato tutto)
        if e[u] > 0 and u != s and u != t:
            if u not in active_set:
                active_nodes.append(u)
                active_set.add(u)

    # Calcolo Risultato Finale
    flow = {}
    
    # Calcoliamo il flusso per ogni arco originale
    for u, v, data in R.edges(data=True):
        original_cap = data.get('capacity', 0)
        if original_cap > 0:
    # Il flusso è (capacità originale - residuo attuale)
            flow[(u, v)] = original_cap - R[u][v]['residual']
            
    # Calcoliamo il Max Flow sommando i flussi uscenti da s
    max_flow = sum(flow.get((s, v), 0) for v in R.neighbors(s))

    return max_flow, flow


