import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection(name="sentences")

#obtenim les 10 primers files del documentn
docs = collection.peek(10)
first_10_sentences = docs["documents"]  # lista de las primeras frases
print(first_10_sentences)
#para cada una de esas frases buscamos las 2 mas parecidas
results = collection.query(
    query_texts=first_10_sentences,
    n_results=2
)

#ValueError: Non-empty lists are required for ['documents'] in query.

print(results)




