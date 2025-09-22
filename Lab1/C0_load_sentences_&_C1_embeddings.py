import statistics

import chromadb
from chromadb.utils import embedding_functions

import csv, time

#forcem aquest model de transformer per a que el rendiment sigui similar als scripts de P0,p1 i p2, sino triga 10 vegades mes
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")


client = chromadb.PersistentClient(path="./chroma_db")
client.delete_collection(name="sentences")

collection = client.get_or_create_collection(name="sentences",
                                             embedding_function=sentence_transformer_ef
                                             )

texts = []
with open("bookcorpus_10k_sentences.csv", "r", encoding="utf8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        texts.append(r["text"])

# Define el tamaño del lote
batch_size = 512  # Puedes ajustar este valor

times = []
for i in range(3):
    collection.delete(where={'id': {'$ne': ''}})

    start_time = time.time()

    # Itera sobre los datos en baches
    ids = [str(k) for k in range(len(texts))]

    for j in range(0, len(texts), batch_size):
        batch_texts = texts[j:j + batch_size]
        batch_ids = ids[j:j + batch_size]

        # Agrega el lote a la colección
        collection.add(
            documents=batch_texts,
            ids=batch_ids
            )

    end_time = time.time()
    elapsed = end_time - start_time
    times.append(elapsed)

# Estadísticas
print("Max:", max(times))
print("Min:", min(times))
print("Avg:", sum(times) / len(times))
print("Standard Deviation:", statistics.stdev(times))