import streamlit as st
from PIL import Image
import io
import base64
from typing import Optional, Tuple

class ImageUtils:
    """Utility functions for image handling"""
    
    @staticmethod
    def resize_image(image: Image.Image, max_size: Tuple[int, int] = (1024, 1024)) -> Image.Image:
        """Resize image while maintaining aspect ratio"""
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image
    
    @staticmethod
    def image_to_base64(image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()
    
    @staticmethod
    def base64_to_image(base64_string: str) -> Image.Image:
        """Convert base64 string to PIL Image"""
        image_data = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(image_data))
    
    @staticmethod
    def validate_image(uploaded_file) -> Optional[Image.Image]:
        """Validate and load uploaded image"""
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                return image
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")
                return None
        return None
    
    @staticmethod
    def display_image_with_download(image: Image.Image, caption: str = "", key: str = ""):
        """Display image with download button"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.image(image, caption=caption, use_column_width=True)
        
        with col2:
            # Convert to bytes for download
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
            
            st.download_button(
                label="📥 Download",
                data=buffer.getvalue(),
                file_name=f"generated_image_{key}.png",
                mime="image/png",
                key=f"download_{key}"
            )
