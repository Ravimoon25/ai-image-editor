import requests
import streamlit as st
from PIL import Image
import io
import time
from typing import Optional, Dict, Any
import base64

class ImageGenerator:
    """Handle actual image generation using various APIs"""
    
    def __init__(self):
        self.huggingface_api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        
    def generate_with_huggingface(self, prompt: str, hf_token: Optional[str] = None) -> Optional[Image.Image]:
        """Generate image using Hugging Face Inference API"""
        
        headers = {}
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "num_inference_steps": 20,
                "guidance_scale": 7.5,
                "width": 512,
                "height": 512
            }
        }
        
        try:
            with st.spinner("🎨 Generating image... This may take 30-60 seconds"):
                response = requests.post(
                    self.huggingface_api_url, 
                    headers=headers, 
                    json=payload,
                    timeout=120
                )
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    return image
                elif response.status_code == 503:
                    st.warning("⏳ Model is loading, please wait a moment and try again...")
                    return None
                else:
                    st.error(f"Generation failed: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            st.error(f"Error generating image: {str(e)}")
            return None
    
    def generate_with_replicate(self, prompt: str, replicate_token: str) -> Optional[Image.Image]:
        """Generate image using Replicate API (requires API key)"""
        # Placeholder for Replicate integration
        st.info("Replicate integration coming soon!")
        return None
    
    def generate_with_dalle(self, prompt: str, openai_key: str) -> Optional[Image.Image]:
        """Generate image using DALL-E API (requires OpenAI API key)"""
        # Placeholder for DALL-E integration
        st.info("DALL-E integration coming soon!")
        return None
