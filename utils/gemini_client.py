from google import genai
import streamlit as st
from typing import Optional
from PIL import Image
import io
import base64

class GeminiClient:
    """Wrapper class for Gemini API interactions"""
    
    def __init__(self, api_key: str):
        """Initialize Gemini client with API key"""
        if not api_key:
            raise ValueError("API key is required")
        
        # Set the API key in environment-like way for genai.Client()
        import os
        os.environ['GEMINI_API_KEY'] = api_key
        
        self.client = genai.Client()
        self.conversation_history = []
    
    def generate_image(self, prompt: str) -> Optional[str]:
        """Generate image using Gemini Flash"""
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=f"Generate an image: {prompt}"
            )
            return response.text
        except Exception as e:
            st.error(f"Error generating image: {str(e)}")
            return None
    
    def send_message(self, message: str, image: Optional[Image.Image] = None) -> str:
        """Send a message to Gemini"""
        try:
            if image:
                # Convert image to format Gemini can understand
                contents = [message, image]
            else:
                contents = message
                
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=contents
            )
            return response.text
        except Exception as e:
            st.error(f"Error communicating with Gemini: {str(e)}")
            return "Sorry, I encountered an error processing your request."
    
    def analyze_image(self, image: Image.Image, prompt: str = "Describe this image") -> str:
        """Analyze an image with a specific prompt"""
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[prompt, image]
            )
            return response.text
        except Exception as e:
            st.error(f"Error analyzing image: {str(e)}")
            return "Sorry, I couldn't analyze this image."
    
    @staticmethod
    def validate_connection(api_key: str) -> bool:
        """Test if the API key works"""
        try:
            import os
            os.environ['GEMINI_API_KEY'] = api_key
            client = genai.Client()
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents="Hello"
            )
            return True
        except Exception:
            return False
