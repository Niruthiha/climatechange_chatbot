### Climate Change Chatbot
## Overview
The Climate Change Chatbot is an interactive tool designed to provide users with information about climate change using advanced natural language processing techniques. By leveraging a Retrieval-Augmented Generation (RAG) approach, this chatbot utilizes a combination of a vector database and OpenAI's language model to deliver accurate and relevant responses based on user queries.

## Features
- Natural Language Understanding: The chatbot understands user queries about climate change and retrieves relevant information from a preprocessed dataset.
- Dynamic Responses: Utilizing the GPT-3.5-turbo model, the chatbot generates context-aware responses based on the queried information.
- Easy to Use: Users can simply input their questions into a text field to receive informative answers.

## Technologies Used
- Streamlit: For building the web interface for user interactions.
- OpenAI API: To generate responses using the GPT-3.5-turbo model.
- ChromaDB: A vector database used for efficient information retrieval.
- Python 3.8 or higher
- Required Python packages listed in requirements.txt

## Data Source
The data used for the Climate Change Chatbot is derived from the IPCC AR6 WGII Technical Summary (IPCC_AR6_WGII_TechnicalSummary.pdf). This technical summary complements and expands on the key findings of the Working Group II contribution to the Sixth Assessment Report (AR6), providing essential insights into climate change impacts and responses.

## Evaluating the Model
The script evaluates the fine-tuned model based on several metrics. It uses ChromaDB for document retrieval and the SentenceTransformers library for embedding calculations. Ensure you have the correct path to your ChromaDB storage and adjust the model ID as necessary.

## Setup
1. Clone the Repository
2. Set Environment Variable: Make sure to set your OpenAI API key in your environment: export OPENAI_API_KEY="your_api_key_here"
3. Running the Chatbot: To run the chatbot, execute the following command: streamlit run app.py

## Create a Virtual Environment
It’s recommended to use a virtual environment to manage project dependencies. 

## Install Required Libraries
Once the virtual environment is activated, install the required dependencies using the requirements.txt file. 
This will install all necessary libraries, including:
- openai: For accessing OpenAI's API.
- langchain: For text splitting and management.
- chromadb: For creating and querying the vector database.
- pypdf: For reading PDF documents.

## Fine-Tuning the Model
1. The script to fine-tune the model and evaluate its performance is fine_tune_model.py.
2. Upload Training Data
3. Ensure your training data is in the data/ directory. The data should be in JSONL format.
4. Fine-Tune the Model
   
I got confirmation email from oepn ai like this

![image](https://github.com/user-attachments/assets/a866e32d-6cda-4246-b39c-f700339488a7)

## Demo
https://youtu.be/Xx-mtNaRHeI

## Sample Responses
![image](https://github.com/user-attachments/assets/7ebbdfbb-0b84-4e06-8fe5-5795ee9a0ab2)
![image](https://github.com/user-attachments/assets/52ac59b1-50e8-4799-9760-1016955f4eca)
![image](https://github.com/user-attachments/assets/872c5dba-2681-4131-b8dd-ff8ea91463b7)



