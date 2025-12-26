# chatbot_logic.py
from sentence_transformers import util
import torch
import numpy as np

def get_chatbot_response(user_query, question_embeddings_kb, questions_kb, responses_content_kb, response_types_kb, explanations_kb, model_obj, similarity_threshold=0.8):
    """
    Processes a user query to find the most semantically similar question in the knowledge base.
    Retrieves the associated response content, type, and optional explanation.
    Always provides embedding details for the most similar KB question, regardless of threshold.

    Args:
        user_query (str): The text query from the user.
        question_embeddings_kb (torch.Tensor): Pre-computed embeddings of KB questions.
        questions_kb (list): List of KB question strings.
        responses_content_kb (list): List of KB response content (text, code, etc.).
        response_types_kb (list): List of KB response types (e.g., "text", "code").
        explanations_kb (list): List of optional KB explanation strings.
        model_obj (SentenceTransformer): The loaded Sentence Transformer model.
        similarity_threshold (float): The minimum cosine similarity score for a confident match.

    Returns:
        dict: A dictionary containing details about the response, including:
              - user_query_embedding (np.array): Embedding of the user's query.
              - matched_question (str): The most similar question found in the KB.
              - matched_question_embedding (np.array): Embedding of the most similar KB question.
              - similarity_score (float): Cosine similarity between user query and matched KB question.
              - response_content (str): The main content for the chatbot's reply.
              - response_type (str): The type of content (e.g., "text", "code").
              - explanation (str): Optional explanation for the response.
    """
    # Generate embedding for the user's query
    user_query_embedding = model_obj.encode(user_query, convert_to_tensor=True)

    # Calculate cosine similarity between user query and all KB questions
    cosine_scores = util.pytorch_cos_sim(user_query_embedding, question_embeddings_kb)[0]
    max_similarity_score = torch.max(cosine_scores).item()
    most_similar_question_idx = torch.argmax(cosine_scores).item()

    response_info = {
        "user_query_embedding": user_query_embedding.cpu().numpy(),
        "matched_question": "",
        "matched_question_embedding": None,
        "similarity_score": round(max_similarity_score, 4),
        "response_content": "",
        "response_type": "text", # Default type
        "explanation": ""
    }

    # Always populate matched_question_embedding with the actual embedding of the most similar question
    response_info["matched_question_embedding"] = question_embeddings_kb[most_similar_question_idx].cpu().numpy()

    # Determine response based on similarity threshold
    if max_similarity_score >= similarity_threshold:
        response_info["matched_question"] = questions_kb[most_similar_question_idx]
        response_info["response_content"] = responses_content_kb[most_similar_question_idx]
        response_info["response_type"] = response_types_kb[most_similar_question_idx]
        response_info["explanation"] = explanations_kb[most_similar_question_idx]

    else:
        # Fallback response if no strong match is found
        response_info["response_content"] = user_query # Pass the user query to the controller
        response_info["matched_question"] = "N/A (No strong match)"
        response_info["response_type"] = "generative"
        response_info["explanation"] = ""

    return response_info