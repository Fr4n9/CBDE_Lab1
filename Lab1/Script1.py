from sentence_transformers import SentenceTransformer

#Codifica los embedded de cada posicion del array que es una frase y devuelve 384 valores float para cada valor
# Ejemplo sentences = ["This is an example sentence", "Each sentence is converted"]

sentences = [""]
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(sentences)

########################################################################################


# P1_generate_store_embeddings_2tables.py
from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import execute_values
import numpy as np, time, statistics

model = SentenceTransformer("all-MiniLM-L6-v2")
conn = psycopg2.connect(...)
cur = conn.cursor()
cur.execute("ALTER TABLE sentences ADD COLUMN IF NOT EXISTS embedding double precision[];")
conn.commit()

batch_size = 256
cur.execute("SELECT id, sentence_text FROM sentences ORDER BY id")
rows = cur.fetchall()

times_gen = []
times_db = []
for i in range(0, len(rows), batch_size):
    batch = rows[i:i+batch_size]
    ids = [r[0] for r in batch]
    texts = [r[1] for r in batch]
    t0 = time.perf_counter()
    embeds = model.encode(texts, convert_to_numpy=True, batch_size=64)
    times_gen.append(time.perf_counter() - t0)

    # prepare temp table and update
    t0 = time.perf_counter()
    cur.execute("CREATE TEMP TABLE tmp_emb (id INT, embedding double precision[]);")
    tuples = [(int(id_), list(map(float, emb))) for id_, emb in zip(ids, embeds)]
    execute_values(cur, "INSERT INTO tmp_emb (id, embedding) VALUES %s", tuples)
    cur.execute("UPDATE sentences s SET embedding = t.embedding FROM tmp_emb t WHERE s.id = t.id")
    conn.commit()
    times_db.append(time.perf_counter() - t0)

print("embedding gen stats:", min(times_gen), max(times_gen), statistics.mean(times_gen), statistics.pstdev(times_gen))
print("embedding db stats:", min(times_db), max(times_db), statistics.mean(times_db), statistics.pstdev(times_db))
cur.close(); conn.close()


