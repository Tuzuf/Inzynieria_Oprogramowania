import chromadb
import ollama
from read_data import read_data
import json 

data = read_data("data\store\sklep_spozywczy.xlsx")
database = "sklep_spozywczy"
client = chromadb.HttpClient(host='localhost', port=8000)

#Remove old collection from database
try:
     client.delete_collection(database)
except:
     pass
#Create new collection
collection = client.create_collection(database)

# Calculate embeddings for the 'Produkt' column
embeddings = []
for ind, row in data.iterrows():
  produkt = row["Produkt"]
  kategoria = row["Kategoria produktu"]
  data_to_emb = json.dumps({"Produkt": produkt, "Kategoria produktu": kategoria})
  print("Calculating embedding for", data_to_emb)
  response = ollama.embeddings(model="mxbai-embed-large", prompt=data_to_emb)
  embeddings.append(response["embedding"])
# add embeddings do dataframe
data["embeddings"] = embeddings
# Add embeddings and other columns to the collection
for i, row in data.iterrows():
  info_columns = ['Produkt', 'Cena', 'Nazwa alejki', 'Numer alejki', 'Półka', 'Kategoria produktu']
  embedding = row["embeddings"]
  document = json.dumps({col: row[col] for col in info_columns})
  collection.add(
    ids=[str(i)],
    embeddings=[embedding],
    documents=[document]
  )
