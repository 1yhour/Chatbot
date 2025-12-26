# knowledge_base_manager.py
import pandas as pd
from sentence_transformers import SentenceTransformer
import torch
import numpy as np
import os
import sys

def load_knowledge_base_and_model(excel_file_name='knowledge_base.xlsx'):
    """
    Loads the knowledge base from an Excel file and the Sentence Transformer model.
    Pre-computes embeddings for all questions in the knowledge base.

    Returns:
        tuple: Contains lists of questions, response content, response types,
               explanations, pre-computed question embeddings, and the model object.
               Returns None for all if an error occurs during loading.
    """
    questions = []
    responses_content = []
    response_types = []
    explanations = []
    global_question_embeddings = None
    model = None

    # Determine the full path to the Excel file
    script_dir = os.path.dirname(__file__)
    full_excel_path = os.path.join(script_dir, excel_file_name)

    try:
        # Read the Excel file into a pandas DataFrame
        kb_df = pd.read_excel(full_excel_path)

        # Extract data from specified columns
        questions = kb_df['question'].tolist()
        responses_content = kb_df['response_content'].tolist()
        response_types = kb_df['response_type'].tolist()
        
        # Explanation column is optional; fill missing values with empty strings
        if 'explanation' in kb_df.columns:
            explanations = kb_df['explanation'].fillna('').tolist()
        else:
            explanations = [''] * len(questions)

        print(f"DEBUG: Knowledge base loaded successfully from '{full_excel_path}' with {len(questions)} entries.")

    except FileNotFoundError:
        print("File Not Found", f"The knowledge base file '{excel_file_name}' was not found at '{full_excel_path}'.\nPlease ensure it's in the same directory as the script.")
        sys.exit(1)
    except KeyError as e:
        print("Data Error", f"Missing expected column in '{excel_file_name}'.\nEnsure 'question', 'response_content', 'response_type' columns exist, and optionally 'explanation'. Error: {e}")
        sys.exit(1)
    except ImportError:
        print("Missing Dependency", "The 'openpyxl' library is required to read Excel files.\nPlease install it: pip install openpyxl")
        sys.exit(1)
    except Exception as e:
        print("Loading Error", f"Failed to load knowledge base from Excel: {e}\nPlease check the file format and content.")
        sys.exit(1)

    try:
        # Load the Sentence Transformer model
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("DEBUG: Model loaded successfully.")
    except Exception as e:
        print("Model Load Error", f"Failed to load SentenceTransformer model: {e}\nPlease ensure you have an internet connection and the model can be downloaded.")
        sys.exit(1)

    # Create embeddings for all knowledge base questions
    global_question_embeddings = model.encode(questions, convert_to_tensor=True)
    print("DEBUG: Embeddings created successfully.")

    return questions, responses_content, response_types, explanations, global_question_embeddings, model