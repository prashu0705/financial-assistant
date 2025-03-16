from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyATX4MZX9dwaSLkLMmunRAo7s2fowV0C_Q")  # Replace with your actual API key

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

# Chatbot endpoint
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get user input and session ID from the request
        user_input = request.json.get("message")
        session_id = request.json.get("session_id")
        
        if not user_input or not session_id:
            return jsonify({"error": "Missing message or session_id"}), 400
        
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
        
        # Return the response
        return jsonify({"response": response.text})
    
    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
