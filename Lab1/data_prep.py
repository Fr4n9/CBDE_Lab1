from datasets import Dataset

# carga el fragmento arrow
ds = Dataset.from_file("bookcorpus-train.arrow")

# a pandas y a csv
df = ds.to_pandas()
df.head(10000).to_csv("bookcorpus_10k_sentences.csv", index=False)



