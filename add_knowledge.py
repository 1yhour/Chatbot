# add_knowledge.py
import pandas as pd
import os
# The 'tkinter.messagebox' import is no longer needed.

def append_to_knowledge_base(question, response_content, response_type, explanation):
    """
    Appends a new Q&A pair to the knowledge base Excel file.
    """
    excel_file_name = 'knowledge_base.xlsx'
    script_dir = os.path.dirname(__file__)
    full_excel_path = os.path.join(script_dir, excel_file_name)

    if not os.path.exists(full_excel_path):
        # --- CHANGE THIS ---
        print(f"ERROR: Cannot add knowledge. The file '{excel_file_name}' was not found.")
        return

    try:
        # Read the existing data
        df = pd.read_excel(full_excel_path)

        # Create a new DataFrame for the new data
        new_data = {
            'question': [question],
            'response_content': [response_content],
            'response_type': [response_type],
            'explanation': [explanation]
        }
        new_df = pd.DataFrame(new_data)

        # Concatenate the existing and new data
        updated_df = pd.concat([df, new_df], ignore_index=True)

        # Write the updated DataFrame back to the Excel file
        updated_df.to_excel(full_excel_path, index=False)
        print("Successfully added new knowledge from user feedback.")
        
    except Exception as e:
        # --- AND CHANGE THIS ---
        print(f"ERROR: Failed to add new knowledge to the Excel file: {e}")