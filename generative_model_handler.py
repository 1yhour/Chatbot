#generative_model_handler.py
#handle the generative model interactions

import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

class GenerativeModelHandler:
    def __init__(self):
        """Initializes the generative model."""
        self.api_key_set = False
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.api_key_set = True
            print("DEBUG: Google Generative AI configured successfully.")
        else:
            # Configure with a placeholder to prevent crashes
            genai.configure(api_key="placeholder")
            self.model = None
            print("Warning: GOOGLE_API_KEY not found. Generative features will be disabled.")
            
    def generate_response(self, user_query):
        """
        Sends a query to the generative model and handles the response.
        
        Args:
            user_query (str): The user's input query.
            
        Returns:
            A tuple (response_type, content, explanation) or an error message.
        """
        if not self.api_key_set:
            return 'text', "I'm sorry, my generative model is not configured. Please set a valid GOOGLE_API_KEY.", ''

        try:
            # Modify the prompt to ask the model to include explanation tags
            full_prompt = (
                f"{user_query}. If the response contains code, please enclose it in "
                f"markdown code blocks (e.g., ```python\n# code here\n```). "
                f"If you provide an explanation, please enclose it in [Explanation] and [/Explanation] tags."
            )
            
            response = self.model.generate_content(full_prompt)
            response_text = response.text
            
            # Use our helper function to classify and split the response
            return classify_and_split_response(response_text)
            
        except Exception as e:
            error_message = f"An error occurred with the generative model: {e}"
            return 'error', error_message, ''
            
# Helper function outside the class
def classify_and_split_response(response_text):
    """
    Analyzes the response text to determine if it contains a code block and an explanation.
    
    Returns: A tuple (response_type, content, explanation)
    """
    code = ""
    explanation = ""
    content = response_text
    response_type = 'text'

    # Regex to find a code block (e.g., ```...```)
    code_block_match = re.search(r'```(?:\w+)?\s*([\s\S]*?)```', content)
    
    # Regex to find an explanation block
    explanation_block_match = re.search(r'\[Explanation\]([\s\S]*?)\[/Explanation\]', content)

    if code_block_match:
        code = code_block_match.group(1).strip()
        response_type = 'code'
        # The content is everything except the code block
        content = re.sub(r'```[\s\S]*?```', '', content, flags=re.MULTILINE).strip()
        
    if explanation_block_match:
        explanation = explanation_block_match.group(1).strip()
        # The content is everything except the explanation block
        content = re.sub(r'\[Explanation\][\s\S]*?\[/Explanation\]', '', content, flags=re.MULTILINE).strip()

    # If code was found, but there's a remaining explanation, use that.
    # Otherwise, the content is just the remaining text.
    if code:
        # If there's an explanation and a code block, the 'content' variable might still have some remaining text. 
        # We'll use the explanation and code, and ignore the rest of the text.
        return response_type, code, explanation
    else:
        # No code block, so the content is the main response text. The explanation might still be present.
        return response_type, content, explanation