# pg vector té el calcul de distancies integrat
import psycopg2, time, statistics

num_runs = 5
execution_times = []
query_ids = list(range(1, 11))  # por ejemplo, frases con id 1 al 10
print(f"Executant el procés complet {num_runs} vegades...")

# Configurar pgvector una sola vez
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost"
)
cur = conn.cursor()


for run in range(num_runs):
    start_time = time.time()

    results_cosine = {}
    results_euclidean = {}
    for qid in query_ids:
        # Cosine similarity
        cur.execute("""
           SELECT id,text FROM sentences WHERE id != %s ORDER BY embedding <=> (SELECT embedding FROM sentences WHERE id = %s ) LIMIT 2;
        """, (qid,qid))
        results_cosine[qid] = cur.fetchall()

        # Euclidean distance
        cur.execute("""
            SELECT id,text FROM sentences WHERE id != %s ORDER BY embedding <-> (SELECT embedding FROM sentences WHERE id = %s ) LIMIT 2;
        """, (qid,qid))
        results_euclidean[qid] = cur.fetchall()

    end_time = time.time()
    duration = end_time - start_time
    execution_times.append(duration)
    print(f"Execució {run + 1}: Durada total = {duration:.4f} segons")
cur.close()

# Estadísticas
print("\n--- Resum de Rendiment Complet ---")
print(f"Temps Mínim: {min(execution_times):.4f} segons")
print(f"Temps Màxim: {max(execution_times):.4f} segons")
print(f"Temps Mitjà: {sum(execution_times) / len(execution_times):.4f} segons")
print(f"Desviació Estàndard: {statistics.stdev(execution_times):.4f} segons")
print (results_cosine)
print(results_euclidean)

