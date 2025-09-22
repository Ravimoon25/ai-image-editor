from google import genai
from google.genai import types
import streamlit as st
from typing import Optional
import PIL.Image

class GeminiClient:
    """Fixed Gemini client based on working code pattern"""
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash-image-preview"
    
    def generate_image(self, prompt: str) -> Optional[PIL.Image.Image]:
        """Generate image using correct API method"""
        try:
            # Use generate_content, not generate_image
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    safety_settings=[
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE,
                        )
                    ],
                    response_modalities=['Text', 'Image']
                )
            )
            
            # Extract image from response parts
            for part in response.parts:
                if hasattr(part, 'as_image') and part.as_image():
                    return part.as_image()
            
            return None
            
        except Exception as e:
            st.error(f"Generation error: {str(e)}")
            return None
    
    @staticmethod
    def validate_connection(api_key: str) -> bool:
        """Test connection"""
        try:
            client = genai.Client(api_key=api_key)
            # Simple test call
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents="Hello"
            )
            return True
        except:
            return False
