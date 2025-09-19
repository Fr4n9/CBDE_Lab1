# P1_generate_store_embeddings.py
from numpy.ma.extras import average
from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import execute_values
import numpy as np
import time
import statistics

# Asegúrate de tener la conexión a tu base de datos con los datos correctos

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost"  # , port=5432 si hace falta
)
cur = conn.cursor()

# Se añade la columna 'embedding' si no existe.
cur.execute("ALTER TABLE sentences ADD COLUMN IF NOT EXISTS embedding double precision[];")
conn.commit()

# Carga el modelo de Hugging Face
model = SentenceTransformer("all-MiniLM-L6-v2")

# Selecciona todas las oraciones de la tabla
cur.execute("SELECT id, text FROM sentences")
rows = cur.fetchall()

batch_size = 256
times = []
for j in range(5):
    # Medir el tiempo de generación de embeddings
    # limpiar tabla antes de cada inserción
    start_time = time.time()
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        ids = [r[0] for r in batch]
        texts = [r[1] for r in batch]
        # Medir el tiempo de generación de embeddings
        embeds = model.encode(texts, convert_to_numpy=True)

        # Preparar los datos para la actualización
        # La lista de tuplas debe ser (vector, id) para que el UPDATE funcione
        # De esta forma, el 'id' se utiliza para identificar la fila a actualizar
        updates = [(list(map(float, emb)), id_) for id_, emb in zip(ids, embeds)]

        # Medir el tiempo de actualización de la base de datos
        #t0 = time.perf_counter()
        execute_values(
            cur,
            "UPDATE sentences s SET embedding = t.embedding FROM (VALUES %s) AS t (embedding, id) WHERE s.id = t.id",
            updates
        )
        conn.commit()
    end_time = time.time()
    elapsed = end_time - start_time
    times.append(elapsed)

# Estadísticas
print("Max:", max(times))
print("Min:", min(times))
print("Avg:", sum(times)/len(times))

cur.close()
conn.close()

