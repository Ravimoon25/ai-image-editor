import os
from typing import Optional

class Settings:
    """Application settings and configuration"""
    
    # API Configuration
    GEMINI_MODEL = "gemini-1.5-flash"
    
    # Image settings
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
    SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "webp"]
    
    # Conversation settings
    MAX_CONVERSATION_LENGTH = 20
    
    @staticmethod
    def get_gemini_api_key() -> Optional[str]:
        """Get Gemini API key from environment or session state"""
        import streamlit as st
        return st.session_state.get('gemini_api_key') or os.getenv('GEMINI_API_KEY')
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Basic API key validation"""
        return api_key and len(api_key) > 20 and api_key.startswith('AI')
