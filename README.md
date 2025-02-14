Projekt chatbota wykonanny na przedmiot Inżynieria Oprogramowania.
# Instructions

In order to make any changes configure vs studio and git using

git config --global user.name "Your Name"
git config --global user.email "youremail@yourdomain.com"

# Wymagania

Use below commands in order

## Windows

Download on your PC:
https://ollama.com/download

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

python.exe -m pip install --upgrade 

chroma run --host localhost --port 8000 --path ./embeddings_db

Open new terminal window

.venv\Scripts\activate

ollama pull mxbai-embed-large

python calculate_embeddings.py

In order to use faster chat

streamlit run chat.py

Conversational like UI, its slower

streamlit run chat_conversation.py

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

## Opis funkcji

### read_data.py

### retrieve.py

retrieve - pozwala na promptowanie, zadawanie pytań modelowi

### calculate_embeddings.py

calculate embeddings - liczy embeddingi i zapisuje je w bazie danych chroma
