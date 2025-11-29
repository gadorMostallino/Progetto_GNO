import graph
import pp as pp   
import time
import tqdm as tqdm
import networkx as nx
import os

n = [10,100, 1000, 10000,100000]
max_u = [10,100]
p_edge = [0.1,0.2,0.3,0.4] #con p_edge = 0.1 il grafo sarà molto sparso, con 0.4 molto denso
n_test = 50

results_csv_path = "risultati"

if __name__ == '__main__':

    #crea la cartella se non esiste
    os.makedirs(results_csv_path, exist_ok=True)
    #salva i risultati in un file csv con timestamp in formato: results_YYYY-MM-DD_HH-MM-SS.csv
    results_csv_name = "results_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    full_csv_path = os.path.join(results_csv_path, results_csv_name)
    csv = results_csv_path + results_csv_name

    with open(full_csv_path, 'w') as f:
        f.write("n_nodes;max_capacity;p;time_fpp;time_hlpp;time_elpp;max_flow_fpp;max_flow_hlpp;max_flow_elpp\n")

    with tqdm.tqdm(total=len(n)*len(max_u)*len(p_edge),position=1) as pbar:
        for n_nodes in n:
            for max_capacity in max_u:
                for p in p_edge:
                    time_avg_fpp = 0
                    time_avg_hlpp = 0
                    time_avg_elpp = 0

                    # Contatori per errori
                    errors_f = 0
                    errors_hlpp = 0
                    errors_elpp = 0
                    
                    for i in range(n_test):
                        '''-----------------Create Graph-----------------'''
                        G,s,t = graph.create_directed_flow_graph(n_nodes, max_capacity, p)

                        #debug
                        # --- VERIFICA GROUND TRUTH (NetworkX) ---
                        # Calcoliamo il valore corretto per confrontarlo
                        try: 
                            nx_true_flow = nx.maximum_flow_value(G, s, t, capacity='capacity')
                        except Exception as e:
                            nx_true_flow = -1 # Errore nel calcolo NX (es. grafo non NX)
                        #--------------------------------------------

                        x0 = {(u,v):0 for u,v in G.edges()}
                        R = graph.create_residual_graph(G, x0)
                        '''-----------------Generic Preflow Push-----------------'''
                        start_fpp = time.time()
                        mf_fpp, x_fpp = pp.FIFO_preflow_push_new(R,s,t)
                        end_fpp = time.time()
                        time_fpp = end_fpp - start_fpp
                        time_avg_fpp += time_fpp

                        # Check correttezza ------
                        if mf_fpp != nx_true_flow: errors_fpp += 1

                        if i == 0:
                           status = "OK" if mf_fpp == nx_true_flow else f"ERRORE (atteso {nx_true_flow})"
                           print(f"[FPP] n={n_nodes}, p={p} | Flow: {mf_fpp} | {status}")
                        #-------------------------
                           
                        '''-----------------Highest lable Preflow Push-----------------'''
                        R = graph.create_residual_graph(G, x0)
                        start_hlpp = time.time()
                        mf_hlpp, x_hlpp = pp.highest_label_preflow_push_new(R,s,t)
                        end_hlpp = time.time()
                        time_hlpp = end_hlpp - start_hlpp
                        time_avg_hlpp += time_hlpp

                        # Check correttezza ------
                        if mf_hlpp != nx_true_flow: errors_hlpp += 1

                        if i == 0:
                           status = "OK" if mf_hlpp == nx_true_flow else f"ERRORE (atteso {nx_true_flow})"
                           print(f"[HPP] n={n_nodes}, p={p} | Flow: {mf_hlpp} | {status}")
                        #-------------------------

                        '''-----------------Excess Label Preflow Push-----------------'''
                        R = graph.create_residual_graph(G, x0)
                        start_elpp = time.time()
                        mf_elpp, x_elpp = pp.excess_scaling_preflow_push_new(R,s,t)
                        end_elpp = time.time()
                        time_elpp = end_elpp - start_elpp
                        time_avg_elpp += time_elpp

                        # Check correttezza -----
                        if mf_elpp != nx_true_flow: errors_elpp += 1

                        if i == 0:
                           status = "OK" if mf_elpp == nx_true_flow else f"ERRORE (atteso {nx_true_flow})"
                           print(f"[ELPP] n={n_nodes}, p={p} | Flow: {mf_elpp} | {status}\n")
                        #-------------------------
                    '''-----------------Save Results-----------------'''
                    time_avg_fpp = time_avg_fpp/n_test
                    time_avg_hlpp = time_avg_hlpp/n_test
                    time_avg_elpp = time_avg_elpp/n_test
                

                    with open(full_csv_path, 'a') as f:
                        f.write(f"{n_nodes};{max_capacity};{p};{time_avg_fpp};{time_avg_hlpp};{time_avg_elpp};{mf_fpp};{mf_hlpp};{mf_elpp}\n")
                    pbar.update(1)
    print("DONE")
