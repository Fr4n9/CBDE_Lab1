import psycopg2
import numpy as np
import time
import statistics


def cosine_similarity(vector_a, vector_b):
    # Calcula la similitud del coseno entre dos vectores
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    return dot_product / (magnitude_a * magnitude_b)


def euclidean_distance(vector_a, vector_b):
    # Calcula la distancia euclidiana entre dos vectores
    diferencia = vector_a - vector_b
    return np.sqrt(np.sum(np.square(diferencia)))


num_runs = 5
execution_times = []

print(f"Executant el procés complet {num_runs} vegades...")

for i in range(num_runs):
    start_time = time.time()

    try:
        # Connexió a la base de dades
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost"
        )
        cur = conn.cursor()
        # Selecciona tots els IDs i embeddings de la taula
        cur.execute("SELECT sentence_id, embedding FROM embeddings order by sentence_id ASC")
        all_rows = cur.fetchall()
        cur.close()
        conn.close()

    except psycopg2.OperationalError as e:
        print(f"Error de connexió a la base de dades: {e}")
        print("Assegura't que la base de dades de PostgreSQL estigui en execució.")
        exit()

    # Processa les dades obtingudes de la base de dades
    ids = [r[0] for r in all_rows]
    embs_list = [np.array(r[1], dtype=float) for r in all_rows]
    embs = np.array(embs_list)
    # Selecciona els ids del 1 al 10
    query_ids = ids[0:10]

    # Dicionaris per emmagatzemar els resultats de similitud
    results_cosine = {}
    results_euclidean = {}

    # Bucle principal per a cada vector de consulta
    for i_query, id_query in enumerate(query_ids):
        query_emb = embs[i_query]

        # Llistes per a emmagatzemar les similituds i distàncies
        sims = []
        dists = []
        # Bucle per calcular la similitud i la distància amb tots els altres vectors
        for j in range(len(ids)):
            if j != i_query:
                sim = cosine_similarity(query_emb, embs[j])
                dist = euclidean_distance(query_emb, embs[j])
            else:
                # Exclou el mateix vector de la comparació
                sim = -np.inf
                dist = np.inf
            sims.append(sim)
            dists.append(dist)

        # Troba els índexs dels 2 valors de similitud del cosinus més alts
        top2_cos_idx = np.argsort(sims)[-2:][::-1]
        # Troba els índexs dels 2 valors de distància euclidiana més baixos
        top2_euc_idx = np.argsort(dists)[:2]

        # Emmagatzema els resultats
        results_cosine[id_query] = [(ids[j], sims[j]) for j in top2_cos_idx]
        results_euclidean[id_query] = [(ids[j], dists[j]) for j in top2_euc_idx]

    end_time = time.time()

    duration = end_time - start_time
    execution_times.append(duration)
    print(f"Execució {i + 1}: Durada total = {duration:.4f} segons")

if execution_times:
    min_time = min(execution_times)
    max_time = max(execution_times)
    average_time = sum(execution_times) / len(execution_times)

    if len(execution_times) > 1:
        std_dev = statistics.stdev(execution_times)
    else:
        std_dev = 0.0

    print("\n--- Resum de Rendiment Complet ---")
    print(f"Temps Mínim: {min_time:.4f} segons")
    print(f"Temps Màxim: {max_time:.4f} segons")
    print(f"Temps Mitjà: {average_time:.4f} segons")
    print(f"Desviació Estàndard: {std_dev:.4f} segons")

print("\nResultats de la darrera execució")
print("Resultats per Similitud del Cosenus")
for qid, neighbors in results_cosine.items():
    print(f"Consulta {qid} -> Vectors més propers: {[n[0] for n in neighbors]}")

print("\nResultats per Distància Euclidiana")
for qid, neighbors in results_euclidean.items():
    print(f"Consulta {qid} -> Vectors més propers: {[n[0] for n in neighbors]}")