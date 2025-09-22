import statistics
import psycopg2
from psycopg2.extras import execute_values
import csv, time

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost"
)
cur = conn.cursor()

# 1. Eliminar la tabla existente y crearla con 'id' como INTEGER
cur.execute("""
DROP TABLE IF EXISTS sentences CASCADE;
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS sentences (
    id INTEGER PRIMARY KEY,
    text TEXT
);
""")
conn.commit()

# Llegim el CSV
batch = []
with open("bookcorpus_10k_sentences.csv", "r", encoding="utf8") as f:
    reader = csv.DictReader(f)
    for idx, r in enumerate(reader, 1): # Generar IDs del 1 al 10000
        batch.append((idx, r['text']))  # La tupla ahora tiene (id, texto)

# Medición
times = []
for i in range(5):
    # Limpiamos tabla
    cur.execute("DELETE FROM sentences")
    conn.commit()

    start_time = time.time()
    # Insertamos IDs y textos
    execute_values(cur,
        "INSERT INTO sentences (id, text) VALUES %s",
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
print("Standard Deviation:", statistics.stdev(times))

cur.close()
conn.close()