import streamlit as st
import chromadb
import ollama
import json
import pandas as pd

# Initialize ChromaDB client
client = chromadb.HttpClient(host='localhost', port=8000)
collection = client.get_or_create_collection(name="Store_Inventory")

# Title
st.title("🛒 Chat with Store Bot")

# Sidebar instructions
st.sidebar.title("Instructions")
st.sidebar.write("""
1. Type your query below to ask about products.
2. View the conversation history and responses.
""")

# Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"role": "assistant", "content": "Hi! I'm Store Bot. How can I assist you today?"}
    ]

# Display conversation history
for msg in st.session_state.conversation:
    if msg["role"] == "assistant":
        st.markdown(f"**Store Bot:** {msg['content']}")
    else:
        st.markdown(f"**You:** {msg['content']}")

# Input box for user query
user_input = st.text_input("Type your message:")

# Function to prevent duplicate responses
def prevent_duplicate_response(query):
    # Check if the user input is the same as the last query
    if len(st.session_state.conversation) > 1:
        last_user_input = st.session_state.conversation[-2]["content"]
        if query == last_user_input:
            return True
    return False

# When the user clicks "Send"
if st.button("Send"):
    if user_input.strip():
        # Prevent duplicate responses
        if prevent_duplicate_response(user_input):
            st.warning("You already asked this question. Please try something different.")
        else:
            # Add user query to conversation
            st.session_state.conversation.append({"role": "user", "content": user_input})

            try:
                # Generate embedding for the query
                response = ollama.embeddings(
                    prompt=user_input,
                    model="mxbai-embed-large"
                )

                # Query ChromaDB
                results = collection.query(
                    query_embeddings=[response["embedding"]],
                    n_results=3
                )

                # Parse documents
                documents = results['documents']
                if not documents or len(documents[0]) == 0:
                    bot_reply = "I couldn't find any matching products. Please try a different query."
                else:
                    parsed_documents = []
                    for doc in documents[0]:
                        try:
                            parsed_documents.append(json.loads(doc))
                        except json.JSONDecodeError:
                            pass  # Skip documents that cannot be parsed

                    if not parsed_documents:
                        bot_reply = "The product data seems to be incomplete or invalid."
                    else:
                        # Generate response text
                        bot_reply = "Here are some products I found:\n\n"
                        for doc in parsed_documents:
                            product_name = doc.get("Product", "Unknown Product")
                            description = doc.get("Description", "No description available.")
                            price = doc.get("Price", "Price not listed.")
                            aisle_name = doc.get("Aisle Name", "Not available")
                            aisle_number = doc.get("Aisle Number", "Not available")
                            shelf = doc.get("Shelf", "Not available")
                            product_category = doc.get("Product Category", "Not available")

                            bot_reply += f"- **{product_name}**: (Price: {price}, {aisle_name}, {shelf}, Category: {product_category}, Aisle {aisle_number})\n"

            except Exception as e:
                bot_reply = f"Oops! Something went wrong: {e}"

            # Add bot reply to conversation
            st.session_state.conversation.append({"role": "assistant", "content": bot_reply})
    else:
        st.warning("Please enter a valid message.")
