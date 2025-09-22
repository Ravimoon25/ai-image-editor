import google.genai as genai
import streamlit as st
from typing import Optional, List, Dict, Any
from PIL import Image
import io
import base64

class GeminiClient:
    """Wrapper class for Gemini API interactions"""
    
    def __init__(self, api_key: str):
        """Initialize Gemini client with API key"""
        if not api_key:
            raise ValueError("API key is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat = None
    
    def start_conversation(self) -> None:
        """Start a new conversation"""
        self.chat = self.model.start_chat(history=[])
    
    def send_message(self, message: str, image: Optional[Image.Image] = None) -> str:
        """Send a message to Gemini, optionally with an image"""
        try:
            if image:
                response = self.chat.send_message([message, image])
            else:
                response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            st.error(f"Error communicating with Gemini: {str(e)}")
            return "Sorry, I encountered an error processing your request."
    
    def analyze_image(self, image: Image.Image, prompt: str = "Describe this image") -> str:
        """Analyze an image with a specific prompt"""
        try:
            response = self.model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            st.error(f"Error analyzing image: {str(e)}")
            return "Sorry, I couldn't analyze this image."
    
    @staticmethod
    def validate_connection(api_key: str) -> bool:
        """Test if the API key works"""
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Hello")
            return True
        except Exception:
            return False
