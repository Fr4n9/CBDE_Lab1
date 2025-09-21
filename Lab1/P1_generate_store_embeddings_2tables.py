import statistics

# 2 TABLAS

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

# Carga el modelo de Hugging Face
model = SentenceTransformer("all-MiniLM-L6-v2")

# Selecciona todas las oraciones de la tabla
cur.execute("SELECT id, text FROM sentences")
rows = cur.fetchall()

# Crear tabla si no existe
cur.execute("""
CREATE TABLE IF NOT EXISTS embeddings (
    sentence_id INT PRIMARY KEY REFERENCES sentences(id),
    embedding double precision[]
);
""")
#cur.execute("ALTER TABLE sentences drop column embedding")

conn.commit()

batch_size = 256
times = []

for j in range(5):
    # limpiar tabla antes de cada inserción
    cur.execute("DELETE from embeddings")
    conn.commit()

    start_time = time.time()
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        ids = [r[0] for r in batch]
        texts = [r[1] for r in batch]

        # Generar embeddings
        embeds = model.encode(texts, convert_to_numpy=True)

        # Preparar datos como (id, embedding)
        records = [(id_, emb.tolist()) for id_, emb in zip(ids, embeds)]

        # Inserción masiva
        execute_values(
            cur,
            "INSERT INTO embeddings (sentence_id, embedding) VALUES %s",
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
