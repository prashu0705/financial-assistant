import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyATX4MZX9dwaSLkLMmunRAo7s2fowV0C_Q")  # Replace with your actual API key

# List available models
try:
    models = genai.list_models()
    print("Available Models:")
    for model in models:
        print(f"- Name: {model.name}")
        print(f"  Description: {model.description}")
        print(f"  Supported Methods: {model.supported_generation_methods}")
        print()
except Exception as e:
    print(f"Error: {e}")
