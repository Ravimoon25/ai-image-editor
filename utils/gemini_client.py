from google import genai
import streamlit as st
from typing import Optional
from PIL import Image
import io
import base64

class GeminiClient:
    """Simple wrapper for Gemini API with Imagen"""
    
    def __init__(self, api_key: str):
        import os
        os.environ['GEMINI_API_KEY'] = api_key
        self.client = genai.Client()
    
    def generate_image(self, prompt: str) -> Optional[Image.Image]:
        """Generate actual image using Imagen 4.0"""
        try:
            response = self.client.models.generate_image(
                model="imagen-4.0-generate-001",
                prompt=prompt
            )
            
            # Convert response to PIL Image
            if response and hasattr(response, 'image'):
                # Assuming response contains image data
                image_data = response.image
                if isinstance(image_data, bytes):
                    return Image.open(io.BytesIO(image_data))
                elif isinstance(image_data, str):  # base64
                    image_bytes = base64.b64decode(image_data)
                    return Image.open(io.BytesIO(image_bytes))
            
            return None
            
        except Exception as e:
            st.error(f"Error generating image: {str(e)}")
            return None
    
    def generate_content(self, prompt: str) -> str:
        """Generate text content using Gemini 2.5 Flash"""
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
