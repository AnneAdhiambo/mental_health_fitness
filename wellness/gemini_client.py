import os
import google.generativeai as genai
from django.conf import settings

class GeminiClient:
    def __init__(self):

        api_key = "AIzaSyCkXfRcy0WUaaVi4hVU0qkCB13KNlV7DzE"
        genai.configure(api_key=api_key)
        
        try:
            models = genai.list_models()
            print("Available models:")
            for model in models:
                print(f" - {model.name}")
            
            gemini_models = [m for m in models if "gemini" in m.name.lower() and 
                            "generateContent" in m.supported_generation_methods]
            
            if gemini_models:
                model_name = gemini_models[0].name
                print(f"Using model: {model_name}")
                self.model = genai.GenerativeModel(model_name=model_name)
            else:
                print("No suitable Gemini models found, trying with default name format")
                self.model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
                
        except Exception as e:
            print(f"Error listing models: {e}")
        
            print("Falling back to models/gemini-1.5-pro")
            self.model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
        
    def get_chat_response(self, messages):

        history = []
        
        for msg in messages:
            role = "user" if msg.is_user else "model"
            history.append({"role": role, "parts": [msg.content]})
        
        try:
   
            chat = self.model.start_chat(history=history[:-1] if history else [])
            
            latest_message = history[-1] if history else {"role": "user", "parts": ["Hello"]}
            response = chat.send_message(latest_message["parts"][0])
            return response.text
        except Exception as e:
            error_message = str(e)
            print(f"Gemini API error: {error_message}")
            
            if "models/gemini" in error_message and "not found" in error_message:
                try:
                    print("Trying alternative model format...")
                    alt_model = genai.GenerativeModel(model_name="gemini-pro")
                    chat = alt_model.start_chat(history=history[:-1] if history else [])
                    latest_message = history[-1] if history else {"role": "user", "parts": ["Hello"]}
                    response = chat.send_message(latest_message["parts"][0])
                    return response.text
                except Exception as e2:
                    return f"Error communicating with Gemini API after retry: {str(e2)}"
            
            return f"Error communicating with Gemini API: {error_message}"