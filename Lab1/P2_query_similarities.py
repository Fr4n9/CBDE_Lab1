# P2_query_similarities.py
import psycopg2, numpy as np, time, statistics
import math
from numpy.linalg import norm

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost"  # , port=5432 si hace falta
)
cur = conn.cursor()

#cogemos 10 filas de la tabla con su text y sus embeddings,embeddings que seran del tipo [0.9121,0.12312312,-0.9891291283...]
cur.execute("SELECT id, text, embedding FROM sentences ORDER BY id asc")

#tenemos 10 elementos, los procesamos de forma que buscamos las 2 mas parecidas con el metodo euclidiano?
all_rows = cur.fetchall()
ids = [r[0] for r in all_rows]
texts = [r[1] for r in all_rows]
embs = np.array([np.array(r[2], dtype=float) for r in all_rows])  # shape (N, D)

# elige 10 ids (por ejemplo los primeros 10 o una lista fija)
query_ids = ids[:10]  # asegúrate de identificarlos en el informe





similarities = [(id, cosine_similarity(query, emb)) for id, emb in embeddings]
top2 = sorted(similarities, key=lambda x: x[1], reverse=True)[:2]

#######

def top_k_excluding_self(query_vec, k, metric="cosine"):
    if metric=="cosine":
        # vectorizado
        norms = np.linalg.norm(embs, axis=1)
        qn = np.linalg.norm(query_vec)
        sims = embs.dot(query_vec) / (norms * qn + 1e-12)
        # queremos top por mayor similaridad
        inds = np.argsort(-sims)
    else:  # euclidean
        dists = np.linalg.norm(embs - query_vec, axis=1)
        inds = np.argsort(dists)  # menores primero
    # excluir el propio índice:
    return [i for i in inds if ids[i] != query_id][:k]



times_cos = []
times_euc = []
results = {}
for query_id in query_ids:
    qidx = ids.index(query_id)
    query_vec = embs[qidx]
    # cosine
    t0 = time.perf_counter()
    top2_cos = top_k_excluding_self(query_vec, 2, metric="cosine")
    times_cos.append(time.perf_counter()-t0)
    # euclidean
    t0 = time.perf_counter()
    top2_euc = top_k_excluding_self(query_vec, 2, metric="euclidean")
    times_euc.append(time.perf_counter()-t0)
    results[query_id] = {
        "text": texts[qidx],
        "top2_cos": [(ids[i], texts[i]) for i in top2_cos],
        "top2_euc": [(ids[i], texts[i]) for i in top2_euc]
    }

print("cos times stats", min(times_cos), max(times_cos), statistics.mean(times_cos), statistics.pstdev(times_cos))
print("euc times stats", min(times_euc), max(times_euc), statistics.mean(times_euc), statistics.pstdev(times_euc))
# guarda results y times para el informe
