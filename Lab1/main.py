import datasets

# Carga el dataset de BookCorpus usando su nombre oficial.
# La biblioteca ya sabe dónde encontrar y cómo descargar este dataset.
bookcorpus_dataset = datasets.load_dataset("bookcorpus", split="train")

# Ahora puedes usar el dataset como siempre.
print(bookcorpus_dataset)

# Muestra el primer ejemplo de texto
print(bookcorpus_dataset[0]["text"])

# Guardar en CSV
bookcorpus_dataset.to_csv("bookcorpus.csv")