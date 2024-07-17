### Climate Change Chatbot
## Overview
The Climate Change Chatbot is an interactive tool designed to provide users with information about climate change using advanced natural language processing techniques. By leveraging a Retrieval-Augmented Generation (RAG) approach, this chatbot utilizes a combination of a vector database and OpenAI's language model to deliver accurate and relevant responses based on user queries.

## Features
Natural Language Understanding: The chatbot understands user queries about climate change and retrieves relevant information from a preprocessed dataset.
Dynamic Responses: Utilizing the GPT-3.5-turbo model, the chatbot generates context-aware responses based on the queried information.
Easy to Use: Users can simply input their questions into a text field to receive informative answers.
Technologies Used
Streamlit: For building the web interface for user interactions.
OpenAI API: To generate responses using the GPT-3.5-turbo model.
ChromaDB: A vector database used for efficient information retrieval.
Getting Started
Prerequisites
Python 3.8 or higher
Required Python packages listed in requirements.txt

## Setup
1. Clone the Repository
2. Set Environment Variable: Make sure to set your OpenAI API key in your environment: export OPENAI_API_KEY="your_api_key_here"
3. Running the Chatbot: To run the chatbot, execute the following command: streamlit run app.py
