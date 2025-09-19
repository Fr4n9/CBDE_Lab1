import psycopg2
from psycopg2.extras import execute_values
import csv, time

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost"  # , port=5432 si hace falta
)
cur = conn.cursor()

# Crear tabla si no existe
cur.execute("""
CREATE TABLE IF NOT EXISTS sentences (
    id SERIAL PRIMARY KEY,
    text TEXT
);
""")
conn.commit()

# Leer frases del CSV
batch = []
with open("bookcorpus_10k_sentences.csv", "r", encoding="utf8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        batch.append((r['text'],))   # cada fila como tupla

# Medición
times = []
for i in range(5):
    # limpiar tabla antes de cada inserción
    cur.execute("DELETE FROM sentences")
    conn.commit()

    start_time = time.time()
    execute_values(cur,
        "INSERT INTO sentences (text) VALUES %s",
        batch
    )
    conn.commit()
    end_time = time.time()

    elapsed = end_time - start_time
    times.append(elapsed)
    print(f"Iteración {i+1}: {elapsed:.2f} segundos")

# Estadísticas
print("Max:", max(times))
print("Min:", min(times))
print("Avg:", sum(times)/len(times))

cur.close()
conn.close()
