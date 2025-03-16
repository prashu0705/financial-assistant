import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyATX4MZX9dwaSLkLMmunRAo7s2fowV0C_Q")  

# Initialize the Gemini model
model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

# System prompt to guide Gemini
system_prompt = """
You are a financial assistant that helps users understand investing. 
Provide simple, jargon-free answers to their questions. 
If the user asks about specific investments, provide clear and accurate information.
"""

# Store conversation history (in-memory, replace with a database in production)
conversation_history = {}

# Chat with Gemini
def chat_with_gemini(user_input, session_id):
    try:
        # Initialize session history if it doesn't exist
        if session_id not in conversation_history:
            conversation_history[session_id] = [
                {"role": "user", "parts": [{"text": system_prompt + "\n\nUser: " + user_input}]}
            ]
        else:
            # Add user input to session history
            conversation_history[session_id].append({"role": "user", "parts": [{"text": user_input}]})
        
        # Generate response using Gemini
        response = model.generate_content(conversation_history[session_id])
        
        # Add bot response to session history
        conversation_history[session_id].append({"role": "model", "parts": [{"text": response.text}]})
        
        return response.text
    except Exception as e:
        raise e
