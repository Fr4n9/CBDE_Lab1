import psycopg2, numpy as np, time, statistics
import time

#Tenim la funció que calcula la cosine similarity entre 2 vectos
def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    return dot_product / (magnitude_a * magnitude_b)


def euclidean_distance(vector_a, vector_b):
    diferencia = vector_a - vector_b
    diferencias_al_cuadrado = np.square(diferencia)
    suma_de_cuadrados = np.sum(diferencias_al_cuadrado)
    distancia = np.sqrt(suma_de_cuadrados)
    return distancia

#times = []
#start_time = time.time()
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost"  # , port=5432 si hace falta
)
cur = conn.cursor()

#Agafem de la tauala de ids i embeddings tots els valors de totes les files (les 10k files, crec que es més eficient que fer càlculs complexos entre files en la propia DB)
cur.execute("SELECT sentence_id, embedding FROM embeddings")

all_rows = cur.fetchall()
ids = []
embs_list = []
for r in all_rows:
    ids.append(r[0])
    emb = np.array(r[1], dtype=float)
    embs_list.append(emb)

embs = np.array(embs_list)
query_ids = ids[:10]  # Agafem els 10 primers ids, per a fer les comparacions
#mirem les comparacions entre la query id
times = []
start_time = time.time()
millor_similitud_cosine = -2 # posem -2 o qualsevol valor negatiu ja que la similitud per cosinus va de [-1,1]
millor_id_cosine_1 = 0;
millor_id_cosine_2 = 0;#aqui guardarem la parella d'ids que tinguin millor similitud, després podem fer query a la BD per veure el seu text
millor_id_euclidean_1 = 0;
millor_id_euclidean_2 = 0;
millor_similitud_euclidean = np.inf; #ara busquem la distancia menor, al contrari del cosinus que busquem el major numero
for i in range(len(query_ids)):
    id_query = query_ids[i]
    embeddings_query = embs[i]

    for j in range(len(ids)):
        if (j != i):
            sim = cosine_similarity(embeddings_query, embs[j])
            if sim > millor_similitud_cosine:
                millors_id_cosine_1 = id_query;
                millors_id_cosine_2 = ids[j];
                millor_similitud_cosine= sim
            sim2 = euclidean_distance(embeddings_query, embs[j])
            if sim2 < millor_similitud_euclidean:
                millor_similitud_euclidean = sim2
                millors_id_euclidean_1 = ids[j];
                millors_id_euclidean_2 = id_query;


#aqui ja tenim els valorsde millor similitud
end_time = time.time()
elapsed = end_time - start_time
times.append(elapsed)
print(f"Temps per als 2 metodes: {elapsed:.2f} segons")
print("Els ids de la major similitud de cosinus son", millors_id_cosine_1,millors_id_cosine_2,"amb una similitud de",millor_similitud_cosine)
print("Els ids de la major similitud de euclidean son", millors_id_euclidean_1,millors_id_euclidean_2,"amb una similitud de",millor_similitud_euclidean)


