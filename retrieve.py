import chromadb
import ollama
import json
client = chromadb.HttpClient(host='localhost', port=8000)
collection = client.get_or_create_collection("sklep_spozywczy2")

prompt = "ryż"

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
    print(f"Produkt: {doc['Produkt']}, Cena: {doc['Cena']}, Nazwa alejki: {doc['Nazwa alejki']}, Numer alejki: {doc['Numer alejki']}, Półka: {doc['Półka']}, Kategoria produktu: {doc['Kategoria produktu']}")