import openai
import chromadb
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
import nltk

# Download NLTK data
nltk.download('punkt')

# Load a pre-trained model for text processing
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="db")
chroma_collection = chroma_client.get_or_create_collection("ipcc")

# 1. Relevance of Retrieved Documents
def evaluate_relevance(query, retrieved_docs):
    try:
        query_embedding = embedding_model.encode([query])[0]
        doc_embeddings = embedding_model.encode(retrieved_docs)
        similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
        return np.mean(similarities)
    except Exception as e:
        print(f"Error in relevance evaluation: {e}")
        return None

# 2. Answer Correctness (using a reference answer)
def evaluate_correctness(generated_answer, reference_answer):
    try:
        bleu_scorer = SmoothingFunction()
        bleu_score = sentence_bleu([reference_answer.split()], generated_answer.split(), smoothing_function=bleu_scorer.method1)
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        scores = scorer.score(reference_answer, generated_answer)
        return {
            'BLEU': bleu_score,
            'ROUGE-1': scores['rouge1'].fmeasure,
            'ROUGE-2': scores['rouge2'].fmeasure,
            'ROUGE-L': scores['rougeL'].fmeasure
        }
    except Exception as e:
        print(f"Error in correctness evaluation: {e}")
        return None

# 3. Faithfulness
def evaluate_faithfulness(generated_answer, retrieved_docs):
    try:
        context = ' '.join(retrieved_docs)
        prompt = f"""
        Context: {context}
        Generated Answer: {generated_answer}
        
        On a scale of 1 to 5, how faithful is the generated answer to the given context? 
        Consider:
        1 - Completely unfaithful, contains information not in the context
        5 - Perfectly faithful, all information is derived from the context
        
        Provide your rating and a brief explanation.
        """
        
        response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0125:personal::9wAaEvD7",  # Use your fine-tuned model ID
            messages=[
                {"role": "system", "content": "You are an AI assistant evaluating the faithfulness of answers."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error in faithfulness evaluation: {e}")
        return None

# 4. Robustness
def evaluate_robustness(rag_function, query, num_variations=5):
    try:
        variations = [query]
        for _ in range(num_variations - 1):
            prompt = f"Rephrase this question in a slightly different way: {query}"
            response = openai.ChatCompletion.create(
                model="ft:gpt-3.5-turbo-0125:personal::9wAaEvD7",  # Use your fine-tuned model ID
                messages=[{"role": "user", "content": prompt}]
            )
            variations.append(response.choices[0].message['content'])
        
        answers = [rag_function(q)[0] for q in variations]
        answer_embeddings = embedding_model.encode(answers)
        similarities = cosine_similarity(answer_embeddings)
        upper_tri = similarities[np.triu_indices(len(answers), k=1)]
        
        return np.mean(upper_tri)
    except Exception as e:
        print(f"Error in robustness evaluation: {e}")
        return None

# Main evaluation function
def evaluate_rag_model(rag_function, test_queries, reference_answers):
    results = []
    
    for query, reference_answer in zip(test_queries, reference_answers):
        try:
            generated_answer, retrieved_docs = rag_function(query)
            
            result = {
                'Query': query,
                'Generated Answer': generated_answer,
                'Reference Answer': reference_answer,
                'Relevance': evaluate_relevance(query, retrieved_docs),
                'Correctness': evaluate_correctness(generated_answer, reference_answer),
                'Faithfulness': evaluate_faithfulness(generated_answer, retrieved_docs),
                'Robustness': evaluate_robustness(rag_function, query)
            }
            
            results.append(result)
        except Exception as e:
            print(f"Error processing query '{query}': {e}")
            results.append({
                'Query': query,
                'Generated Answer': None,
                'Reference Answer': reference_answer,
                'Relevance': None,
                'Correctness': None,
                'Faithfulness': None,
                'Robustness': None
            })
    
    return results

# Your RAG function using the fine-tuned model
def rag(query, n_results=5):
    try:
        res = chroma_collection.query(query_texts=[query], n_results=n_results)
        docs = res["documents"][0]
        joined_information = '; '.join([f'{doc}' for doc in docs])
        
        messages = [
            {
                "role": "system",
                "content": "You are a helpful expert on climate change. Your users are asking questions about information contained in attached information. You will be shown the user's question, and the relevant information. Answer the user's question using only this information."
            },
            {"role": "user", "content": f"Question: {query}. \n Information: {joined_information}"}
        ]
        
        response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0125:personal::9wAaEvD7",  # Use your fine-tuned model ID
            messages=messages,
        )
        
        content = response.choices[0].message['content']
        return content, docs
    except Exception as e:
        print(f"Error in RAG function for query '{query}': {e}")
        return None, []

# Example test queries and reference answers
test_queries = [
    "What is the impact of climate change on the ocean?",
    "How does global warming affect biodiversity?",
    # Add more test queries...
]

reference_answers = [
    "Climate change is causing ocean warming, acidification, and deoxygenation, which negatively impact marine ecosystems and biodiversity.",
    "Global warming leads to habitat loss, changes in species distribution, and increased extinction rates, severely affecting biodiversity.",
    # Add corresponding reference answers...
]

# Evaluate the fine-tuned model
evaluation_results = evaluate_rag_model(rag, test_queries, reference_answers)

# Print or process the evaluation results
for result in evaluation_results:
    print(f"Query: {result['Query']}")
    print(f"Generated Answer: {result['Generated Answer']}")
    print(f"Reference Answer: {result['Reference Answer']}")
    print(f"Relevance: {result['Relevance']}")
    print(f"Correctness: {result['Correctness']}")
    print(f"Faithfulness: {result['Faithfulness']}")
    print(f"Robustness: {result['Robustness']}")
    print("\n" + "="*50 + "\n")
