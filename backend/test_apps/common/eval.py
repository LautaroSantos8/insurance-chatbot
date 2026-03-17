from langchain.evaluation import load_evaluator
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_vertexai import VertexAIEmbeddings
# Load LangChain model 

threshold = 0.15

def distance(sentence1, sentence2):
    """
    Calculate the embedding distance between two sentences.

    This function uses Google's Generative AI embeddings to compute the distance between 
    two sentences and evaluate their similarity based on a predefined threshold.

    Parameters:
    - sentence1 (str): The first sentence to compare.
    - sentence2 (str): The second sentence to compare.

    Returns:
    - bool: True if the distance between the sentences is less than the threshold, indicating high similarity.
            False otherwise.
    """
    # Initialize the Google Generative AI Embeddings model for retrieval queries
    embeddings = embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query")
    
    # Load an evaluator for computing embedding distance, using the initialized embeddings model
    evaluator = load_evaluator("embedding_distance", embeddings=embeddings)
    
    # Evaluate the distance between the two sentences using the embeddings
    sentence_eval = evaluator.evaluate_strings(prediction=sentence1, reference=sentence2)['score']
    
    # Print the calculated distance between the sentences
    print("Difference between sentences is:", sentence_eval)
    
    # Return True if the distance is less than the predefined threshold, indicating similarity
    return sentence_eval < threshold

