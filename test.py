import pandas as pd
import matplotlib.pyplot as plt
import io
import os
from matplotlib.ticker import ScalarFormatter
from datetime import datetime

grafici_base_dir = os.path.join(".", "grafici")

# crea la cartella 'grafici' se non esiste
os.makedirs(grafici_base_dir, exist_ok=True)

# creazione cartella per questa esecuzione
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
cartella_corrente = os.path.join(grafici_base_dir, f"run_{timestamp}")
os.makedirs(cartella_corrente)

# modifica il nome del csv sulla base del quale devono essere fatti i grafici
csv_data = "risultati/results_2025-11-29_12-20-09.csv"
df = pd.read_csv(csv_data, sep=';')
print(df.columns)

# Definizioni per il plot
time_columns = ['time_fpp', 'time_hlpp', 'time_elpp']
labels = {
    'time_fpp': 'FIFO Preflow-Push',
    'time_hlpp': 'Highest Label Preflow-Push',
    'time_elpp': 'Excess Label Preflow-Push'
}

# Ciclo per generare i grafi _________________________________________________

# Raggruppa il DataFrame per le colonne 'n_nodes' e 'max_capacity'
# Ogni 'group' nel ciclo conterrà un DataFrame con solo quei valori specifici.
grouped = df.groupby(['n_nodes', 'max_capacity'])

# Crea un formattatore per l'asse Y (notazione scientifica)
formatter = ScalarFormatter(useMathText=True)
formatter.set_powerlimits((-3, 3))

for (n_nodes, max_capacity), group_df in grouped:
    # 1. Crea una nuova figura per questo gruppo
    plt.figure(figsize=(10, 6))

    # 2. Plotta le tre colonne temporali vs. 'p' per questo gruppo
    for col in time_columns:
        plt.plot(group_df['p'], group_df[col], 
                 label=labels[col])


    # 3. Imposta Titolo e Etichette specifici
    title = f'Nodi: {n_nodes} | Capacità Max: {max_capacity}'
    plt.title(title, fontsize=16)
    plt.xlabel('Parametro $p$', fontsize=14)
    plt.ylabel('Tempo di Esecuzione (secondi)', fontsize=14)

    # 4. Aggiunge Legenda, Griglia e formattazione Asse Y
    plt.legend(title='Algoritmo', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.gca().yaxis.set_major_formatter(formatter)
    
    # Imposta i tick dell'asse X in base ai punti dati del gruppo
    plt.xticks(group_df['p'])
    
    # 5. Salva il file con un nome univoco
    filename = f"plot_nodes_{n_nodes}_cap_{max_capacity}.png"
    plt.tight_layout()
    plt.savefig(filename)
    
    # 6. Chiudi la figura per liberare memoria
    plt.close()
    
    print(f"Grafico salvato: {filename}")