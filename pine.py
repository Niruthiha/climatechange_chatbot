
import streamlit as st
import torch
from pinecone import Pinecone
import streamlit as st
from langchain_community.llms import Ollama


llm = Ollama(model="llama3")

# Initialize Pinecone client with your API key
pc = Pinecone(api_key='0c9e1590-5228-4f03-ba6b-3b28592f8a11')

# Connect to your index (replace 'langchain-chatbot' with your actual index name)
index_name = 'langchain-chatbot'
index = pc.Index(index_name)

# Load movies data from movies.txt
def load_movies_data(file_path):
    movies_data = {}
    current_movie = {}
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                key, value = line.split(": ")
                current_movie[key.lower()] = value
            else:
                # End of current movie entry, save it and reset current_movie
                if current_movie:
                    movies_data[current_movie['title'].lower()] = current_movie
                    current_movie = {}
    
    return movies_data



# Function to recommend movies based on user query
def recommend_movies(query_vector, movies_data):
    try:
        # Query the index with the vector
        response = index.query(
            vector=query_vector,
            top_k=5,  # Number of nearest neighbors to retrieve
            include_values=True,
            include_metadata=True
        )

        recommended_movies = []
        if response and "data" in response:
            results = response["data"]
            for result in results:
                movie_id = result['id']
                score = result['score']
                metadata = result['metadata']
                # Fetch movie info from movies_data using the movie_id
                if movie_id in movies_data:
                    movie_info = {
                        'title': movies_data[movie_id]['title'],
                        'genre': movies_data[movie_id]['genre'],
                        'description': movies_data[movie_id]['description'],
                        'score': score,
                        'metadata': metadata
                    }
                    recommended_movies.append(movie_info)
                else:
                    st.warning(f"Movie ID {movie_id} not found in movies_data.")
        
        return recommended_movies

    except Exception as e:
        st.error(f"Error occurred: {e}")
        return []

# Streamlit app UI
st.title("Movie Recommendation 🎬")

# Load movies data from movies.txt
movies_data_file = "movies.txt"
movies_data = load_movies_data(movies_data_file)

# User input for movie recommendation
user_input = st.text_input("Enter a query to get movie recommendations:", "")

if st.button("Prompt"):
    if user_input:
        with st.spinner("Generating ... "):
            st.write(llm.invoke(user_input, stop=['<|eot_id|>']))
            # Adding additional resource links
