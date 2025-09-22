import statistics
import psycopg2, time
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost"
)
cur = conn.cursor()

# Carreguem el model que ens diu el document de HuggingFace
model = SentenceTransformer("all-MiniLM-L6-v2")

# Selecciona todas las oraciones de la tabla
cur.execute("SELECT id, text FROM sentences")
rows = cur.fetchall()
conn.commit()

batch_size = 256
times = []

for j in range(5):
    start_time = time.time()
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        ids = [r[0] for r in batch]
        texts = [r[1] for r in batch]

        # generem embeddings
        embeds = model.encode(texts, convert_to_numpy=True)

        # Preparem els registres en l'ordre correcta
        records = [(ids[k], embeds[k].tolist()) for k in range(len(ids))]

        execute_values(
            cur,
            """
            UPDATE sentences s
            SET embedding = t.embedding
            FROM (VALUES %s) AS t(id, embedding)
            WHERE s.id = t.id
            """,
            records
        )

    conn.commit()
    end_time = time.time()
    elapsed = end_time - start_time
    times.append(elapsed)
    print(f"Iteración {j+1}: {elapsed:.2f} segundos")

# Estadísticas
print("Max:", max(times))
print("Min:", min(times))
print("Avg:", sum(times)/len(times))
print("Standard Deviation:", statistics.stdev(times))

cur.close()
conn.close()