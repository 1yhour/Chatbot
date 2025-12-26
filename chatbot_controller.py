# chatbot_core.py
# This file contains the refactored, UI-independent core logic of the chatbot.

import sys
from chatbot_logic import get_chatbot_response
from knowledge_base_manager import load_knowledge_base_and_model
from generative_model_handler import GenerativeModelHandler
from add_knowledge import append_to_knowledge_base

class ChatbotCore:
    """
    Handles all application logic and state management for the chatbot,
    completely independent of any user interface.
    """
    def __init__(self):
        print("Initializing SmartBot Core...")
        
        # State variables
        self.is_awaiting_feedback = False
        self.last_gen_question = ""
        self.last_gen_response = ""
        self.last_gen_response_type = ""
        self.last_gen_explanation = ""
        
        # Load all necessary models and data
        self._load_data_and_models()
        
        # Initialize the generative model handler
        self.gen_model_handler = GenerativeModelHandler()
        if not self.gen_model_handler.api_key_set:
            # Replaced messagebox with a print warning
            print("\nWARNING: The generative model is disabled because GOOGLE_API_KEY is not set.\n")

        print("SmartBot Core is ready to receive messages.")

    def _load_data_and_models(self):
        """Loads the knowledge base and Sentence Transformer model."""
        try:
            (self.questions, self.responses_content, self.response_types,
             self.explanations, self.global_question_embeddings, self.model) = \
                load_knowledge_base_and_model()

            if self.model is None:
                # Replaced messagebox with print and sys.exit for fatal error
                print("FATAL ERROR: Failed to load the Sentence Transformer model. The application cannot continue.")
                sys.exit(1)

        except Exception as e:
            # Replaced messagebox with print and sys.exit for fatal error
            print(f"FATAL ERROR: An unexpected error occurred while loading data: {e}")
            sys.exit(1)

    def handle_message(self, user_message):
        """
        Processes a user's message, handles feedback, and returns the bot's response string.
        This is the single entry point for all user interaction.
        """
        user_message = user_message.strip()
        if not user_message:
            return "" # Ignore empty input

        # --- Feedback Handling Logic ---
        if self.is_awaiting_feedback:
            self.is_awaiting_feedback = False # Reset state immediately
            
            if user_message.lower() in ["yes", "y", "បាទ", "ចាស"]:
                append_to_knowledge_base(
                    self.last_gen_question,
                    self.last_gen_response,
                    self.last_gen_response_type,
                    self.last_gen_explanation
                )
                self._reload_knowledge_base() # Reload data after adding new knowledge
                return "Thank you! I have added this to my knowledge base."
            else:
                return "Thank you for your feedback. I will not add this to my knowledge base."
        
        # --- Normal Message Handling Logic ---
        response_info = get_chatbot_response(
            user_message,
            self.global_question_embeddings,
            self.questions,
            self.responses_content,
            self.response_types,
            self.explanations,
            self.model
        )

        # --- Generative Fallback Logic ---
        if response_info["response_type"] == "generative":
            self.is_awaiting_feedback = True
            self.last_gen_question = user_message # The original user query
            
            # Call the generative model
            gen_type, gen_content, gen_exp = self.gen_model_handler.generate_response(user_message)
            
            # Store the response for potential feedback
            self.last_gen_response = gen_content
            self.last_gen_response_type = gen_type
            self.last_gen_explanation = gen_exp
            
            # Format the response and ask for feedback
            response_string = f"{gen_content}"
            if gen_exp:
                response_string += f"\n\nExplanation:\n{gen_exp}"
            response_string += "\n\nAre you satisfied with this response? (Yes/No)"
            return response_string
            
        # --- Standard Retrieval Logic ---
        else:
            if response_info["response_type"] == "code":
                response_string = "Here's the code you requested:\n\n" + response_info["response_content"]
                if response_info["explanation"]:
                    response_string += "\n\nExplanation:\n" + response_info["explanation"]
                return response_string
            else: # 'text' or other types
                return response_info["response_content"]

    def _reload_knowledge_base(self):
        """Helper method to reload the knowledge base and notify via console."""
        print("\nUpdating knowledge base, please wait...")
        self._load_data_and_models()
        # Replaced messagebox with a print statement
        print("Knowledge base has been successfully updated.\n")
        
    