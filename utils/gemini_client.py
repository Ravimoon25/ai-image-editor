from google import genai
from google.genai import types
import streamlit as st
from typing import Optional
import PIL.Image

class GeminiClient:
    """Clean Gemini client based on working code"""
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash-image-preview"
    
    def generate_image(self, prompt: str) -> Optional[PIL.Image.Image]:
        """Generate image using the working method from your code"""
        try:
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
            
            for part in response.parts:
                if hasattr(part, 'as_image') and part.as_image():
                    return part.as_image()
            
            return None
            
        except Exception as e:
            st.error(f"Generation error: {str(e)}")
            return None
    
    def edit_image(self, image: PIL.Image.Image, prompt: str) -> Optional[PIL.Image.Image]:
        """Edit image with prompt"""
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[prompt, image],
                config=types.GenerateContentConfig(
                    safety_settings=[
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE,
                        )
                    ]
                )
            )
            
            for part in response.parts:
                if hasattr(part, 'as_image') and part.as_image():
                    return part.as_image()
                    
            return None
            
        except Exception as e:
            st.error(f"Edit error: {str(e)}")
            return None
