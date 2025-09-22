import os
import streamlit as st
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
        """Get Gemini API key from secrets, environment, or session state"""
        # First try Streamlit secrets
        try:
            if "GEMINI_API_KEY" in st.secrets:
                return st.secrets["GEMINI_API_KEY"]
        except:
            pass
        
        # Then try environment variable
        env_key = os.getenv('GEMINI_API_KEY')
        if env_key:
            return env_key
        
        # Finally try session state (manual input)
        return st.session_state.get('gemini_api_key')
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Basic API key validation"""
        return api_key and len(api_key) > 20 and api_key.startswith('AI')
    
    @staticmethod
    def has_api_key_in_secrets() -> bool:
        """Check if API key is available in secrets"""
        try:
            return "GEMINI_API_KEY" in st.secrets and bool(st.secrets["GEMINI_API_KEY"])
        except:
            return False
