import chromadb

client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_or_create_collection(
    name="dataset_collection"
)

def store_chunks(chunks):

    ids = [f"id_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        ids=ids
    )

def search_chunks(query, n_results=3):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results