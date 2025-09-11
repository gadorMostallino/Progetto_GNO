import graph
import preflow_push as pp   
import time
import tqdm as tqdm

#n = [10,100,1000,10000,100000]
n = [10,100,1000]
max_u = [10,100,1000]
p_edge = [0.1,0.2,0.3,0.4]
n_test = 100

results_csv_path = ".//"


if __name__ == '__main__':
    #save results in a csv file with timestamp in format: results_YYYY-MM-DD_HH-MM-SS.csv
    results_csv_name = "results_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    csv = results_csv_path + results_csv_name
    with open(results_csv_name, 'w') as f:
        f.write("n_nodes;max_capacity;p;time_gpp;time_hdpp;time_elpp\n")
    with tqdm.tqdm(total=len(n)*len(max_u)*len(p_edge),position=1) as pbar:
        for n_nodes in n:
            for max_capacity in max_u:
                for p in p_edge:
                    time_avg_gpp = 0
                    time_avg_hdpp = 0
                    time_avg_elpp = 0
                    for i in range(n_test):
                        '''-----------------Create Graph-----------------'''
                        R,s,t = graph.create_directed_flow_graph(n_nodes, max_capacity, p)
                        x0 = {(u,v):0 for u,v in R.edges()}
                        R = graph.create_residual_graph(R, x0)
                        '''-----------------Generic Preflow Push-----------------'''
                        start_gpp = time.time()
                        mf_gpp, x_gpp = pp.generic_preflow_push(R,s,t)
                        end_gpp = time.time()
                        time_gpp = end_gpp - start_gpp
                        time_avg_gpp += time_gpp
                        '''-----------------Highest lable Preflow Push-----------------'''

                        start_hdpp = time.time()
                        mf_hdpp, x_hdpp = pp.highest_lable_preflow_push(R,s,t)
                        end_hdpp = time.time()
                        time_hdpp = end_hdpp - start_hdpp
                        time_avg_hdpp += time_hdpp
                        '''-----------------Excess Label Preflow Push-----------------'''

                        start_elpp = time.time()
                        mf_elpp, x_elpp = pp.excess_scaling_preflow_push(R,s,t)
                        end_elpp = time.time()
                        time_elpp = end_elpp - start_elpp
                        time_avg_elpp += time_elpp

                    '''-----------------Save Results-----------------'''
                    time_avg_gpp = time_avg_gpp/n_test
                    time_avg_hdpp = time_avg_hdpp/n_test
                    time_avg_elpp = time_avg_elpp/n_test

                    with open(results_csv_name, 'a') as f:
                        f.write(f"{n_nodes};{max_capacity};{p};{time_avg_gpp};{time_avg_hdpp};{time_avg_elpp}\n")
                    pbar.update(1)
    print("DONE")
