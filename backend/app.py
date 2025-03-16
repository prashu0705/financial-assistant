from flask import Flask, request, jsonify
from chatbot import chat_with_gemini

app = Flask(__name__)

# Chatbot endpoint
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get user input and session ID from the request
        user_input = request.json.get("message")
        session_id = request.json.get("session_id")
        
        if not user_input or not session_id:
            return jsonify({"error": "Missing message or session_id"}), 400
        
        # Generate response using Gemini
        response = chat_with_gemini(user_input, session_id)
        
        # Return the response
        return jsonify({"response": response})
    
    except Exception as e:
        # Handle errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
