import chromadb

# Conectar al cliente y a la colección
client = chromadb.Client()
collection = client.get_collection(name="sentences")

# Obtener todos los documentos de la colección
all_documents = collection.get()

# Imprimir los datos
# La variable all_documents es un diccionario con las claves 'ids', 'documents', y 'embeddings'
print("--- IDs ---")
print(all_documents['ids'])

print("\n--- Documentos ---")
print(all_documents['documents'])

# Opcional: imprimir los embeddings (pueden ser muchos)
# print("\n--- Embeddings ---")
# print(all_documents['embeddings'])