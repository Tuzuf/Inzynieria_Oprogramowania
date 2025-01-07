# Instructions

# Wymagania

Use below commands in order

## Windows

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

chroma run --host localhost --port 8000 --path ./embeddings_db

Open new terminal window

.venv\Scripts\activate

ollama pull mxbai-embed-large

python calculate_embeddings.py

streamlit run chat.py

## Linux

utworzenie środowiska wirtualnego:
python -m venv .venv
aktywacja:
source .venv/bin/activate
Uruchomienie chroma db:
chroma run --host localhost --port 8000 --path ./embeddings_db
pip install -r requirements.txt
(po aktywacji środowiska)

# Opis kodu

calculate embeddings - liczy embeddingi i zapisuje je w bazie danych chroma
retrieve - pozwala na promptowanie, zadawanie pytań modelowi

Things to be fixed:

Model can't work properly with polish words like róża
