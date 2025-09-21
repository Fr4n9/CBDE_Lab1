import chromadb
import time
import statistics

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("sentences")

num_runs = 5
execution_times = []
#agafem els id dels 10 primers elements per a que coincideixin amb els de PostgreSQL
lista_ids = [str(i) for i in range(11)]
result = collection.get(ids=lista_ids)

#ara agafem els textos dels 10 primers elements
query_texts = result['documents']
print(f"Executing collection.query {num_runs} times to measure performance...")

for i in range(num_runs):
    start_time = time.time()
    results = collection.query(
        query_texts=query_texts,
        n_results=2
    )
    end_time = time.time()

    duration = end_time - start_time
    execution_times.append(duration)

    print(f"Run {i + 1}: Duration = {duration:.4f} seconds")

if execution_times:
    min_time = min(execution_times)
    max_time = max(execution_times)
    std_dev = statistics.stdev(execution_times)
    average_time = sum(execution_times) / len(execution_times)

    print("\n--- Performance Summary ---")
    print(f"Minimum Execution Time: {min_time:.4f} seconds")
    print(f"Maximum Execution Time: {max_time:.4f} seconds")
    print(f"Standard Deviation: {std_dev:.4f} seconds")
    print(f"Average Execution Time: {average_time:.4f} seconds")

print("\nLast query results:")
print(results)



