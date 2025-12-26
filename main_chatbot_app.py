# main_cli.py
from chatbot_controller import ChatbotCore # Import your new refactored class

def run_chatbot_cli():
    """Runs the chatbot in a command-line interface loop."""
    
    chatbot = ChatbotCore()
    print("\n--- Welcome to SmartBot Q&A (CLI Mode) ---")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("SmartBot: Goodbye!")
            break
        
        bot_output = chatbot.handle_message(user_input)
        print(f"SmartBot: {bot_output}")

if __name__ == "__main__":
    run_chatbot_cli()