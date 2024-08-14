#%% packages
import streamlit as st
import os
from pprint import pprint
import chromadb
import openai

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

#%% data prep
chroma_client = chromadb.PersistentClient(path="db")
chroma_collection = chroma_client.get_or_create_collection("ipcc")

#%% Define the RAG function
def rag(query, n_results=5):
    res = chroma_collection.query(query_texts=[query], n_results=n_results)
    docs = res["documents"][0]
    joined_information = ';'.join([f'{doc}' for doc in docs])
    
    # Define the messages for the chat completion
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful expert on climate change. Your users are asking questions "
                "about information contained in attached information. You will be shown the user's "
                "question, and the relevant information. Answer the user's question using only this information."
            )
        },
        {"role": "user", "content": f"Question: {query}. \n Information: {joined_information}"}
    ]
    
    # Create the chat completion using OpenAI's GPT-3.5-turbo model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    
    content = response.choices[0].message['content']
    return content, docs

#%% Streamlit interface
st.header("Climate Change Chatbot")

# Text input field
user_query = st.text_input(
    label="", 
    help="Ask here to learn about Climate Change", 
    placeholder="What do you want to know about climate change?"
)

if user_query:
    rag_response, raw_docs = rag(user_query)

    st.header("RAG Response")
    st.write(rag_response)

# %%
