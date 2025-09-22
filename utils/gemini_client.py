from google import genai
import streamlit as st
from typing import Optional
from PIL import Image

class GeminiClient:
    """Simple wrapper for Gemini API"""
    
    def __init__(self, api_key: str):
        import os
        os.environ['GEMINI_API_KEY'] = api_key
        self.client = genai.Client()
    
    def generate_content(self, prompt: str) -> str:
        """Generate content using Gemini 2.5 Flash"""
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    @staticmethod
    def validate_connection(api_key: str) -> bool:
        try:
            import os
            os.environ['GEMINI_API_KEY'] = api_key
            client = genai.Client()
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents="Hello"
            )
            return True
        except:
            return False
