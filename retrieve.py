import chromadb
import ollama
import json
client = chromadb.HttpClient(host='localhost', port=8000)
collection = client.get_or_create_collection("Store_Inventory")

prompt = "Where can i find bread?"

response = ollama.embeddings(
    prompt=prompt,
    model="mxbai-embed-large"
)

results = collection.query(
    query_embeddings=[response["embedding"]],
    n_results=10
)

documents = results['documents']

parsed_documents = [json.loads(doc) for doc in documents[0]]
for doc in parsed_documents:
    print(f"Product: {doc['Product']}, Price: {doc['Price']}, Aisle Name: {doc['Aisle Name']}, Aisle Number: {doc['Aisle Number']}, Shelf: {doc['Shelf']}, Product Category: {doc['Product Category']}")