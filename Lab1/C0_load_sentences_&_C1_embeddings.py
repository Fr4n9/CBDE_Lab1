import chromadb
import csv, time

client = chromadb.Client()
collection = client.create_collection(name="sentences")

texts = []
with open("bookcorpus_10k_sentences.csv", "r", encoding="utf8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        texts.append(r["text"])

# Define el tamaño del lote
batch_size = 512  # Puedes ajustar este valor

times = []
for i in range(2):
    collection.delete(where={'id': {'$ne': ''}})

    start_time = time.time()

    # Itera sobre los datos en baches
    for j in range(0, len(texts), batch_size):
        batch_texts = texts[j:j + batch_size]
        batch_ids = [str(k) for k in range(j, min(j + batch_size, len(texts)))]

        # Agrega el lote a la colección
        collection.add(
            documents=batch_texts,
            ids=batch_ids
        )

    end_time = time.time()

    elapsed = end_time - start_time
    times.append(elapsed)
    print(f"Iteración {i + 1}: {elapsed:.2f} segundos")

# Estadísticas
print("Max:", max(times))
print("Min:", min(times))
print("Avg:", sum(times) / len(times))