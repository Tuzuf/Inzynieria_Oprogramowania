import streamlit as st
import chromadb
import ollama
import json
import pandas as pd

# Initialize ChromaDB client
client = chromadb.HttpClient(host='localhost', port=8000)
collection = client.get_or_create_collection(name="Store_Inventory")

st.title("Chat with Sklep Spożywczy")

user_input = st.text_input("Ask a question about a product:")

if user_input:
    response = ollama.embeddings(
        prompt=user_input,
        model="mxbai-embed-large"
    )

    results = collection.query(
        query_embeddings=[response["embedding"]],
        n_results=10
    )

    documents = results['documents']
    parsed_documents = [json.loads(doc) for doc in documents[0]]
    df = pd.DataFrame(parsed_documents)

    st.table(df)