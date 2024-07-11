# Chatbot-RAG-Vector-Database
This project implements an adaptive chatbot that leverages Retrieval-Augmented Generation (RAG) for generating personalized recommendations based on user inputs. It combines the capabilities of a Large Language Model (LLM) for natural language understanding with a vector database for efficient data storage and retrieval.
This Streamlit app recommends movies based on user queries using Pinecone for vector search and an LLM for generating prompts or recommendations.

### Features

- **Vector Search:** Utilizes Pinecone's API for efficient vector similarity search.
- **LLM Integration:** Uses a large language model (LLM) for generating text prompts.
- **User Interaction:** Allows users to input queries and receive movie recommendations.

movies.txt A sample dataset containing movie information formatted as: 
  - Title: Movie Title 1
  - Genre: Action
  - Description: This is a description of the movie.
