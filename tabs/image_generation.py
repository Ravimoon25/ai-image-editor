import streamlit as st
from utils.gemini_client import GeminiClient
from utils.image_utils import ImageUtils
import time

def render():
    """Render the Image Generation tab"""
    
    # Check if Gemini client is available
    if not st.session_state.get('gemini_client'):
        st.warning("⚠️ Please configure your Gemini API key in the sidebar first.")
        return
    
    gemini_client = st.session_state.gemini_client
    
    # Initialize tab-specific session state
    if 'gen_conversation' not in st.session_state:
        st.session_state.gen_conversation = []
    
    st.markdown("### 🎨 Generate Images with Gemini Flash")
    st.markdown("Describe the image you want to create using Gemini's native image generation!")
    
    # Two columns: chat and settings
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("⚙️ Generation Settings")
        
        # Style options
        style = st.selectbox(
            "Style",
            ["Photorealistic", "Digital Art", "Oil Painting", "Watercolor", "Sketch", "Cartoon", "Abstract"]
        )
        
        # Quality settings
        quality = st.selectbox(
            "Quality",
            ["Standard", "High Quality", "Professional"]
        )
        
        # Aspect ratio
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            ["Square (1:1)", "Portrait (3:4)", "Landscape (4:3)", "Wide (16:9)"]
        )
        
        st.divider()
        
        # Quick prompt suggestions
        st.subheader("💡 Quick Ideas")
        prompt_suggestions = [
            "A serene mountain landscape at sunset",
            "Portrait of a professional person",
            "Abstract geometric art with vibrant colors", 
            "A cozy coffee shop interior",
            "Futuristic city skyline",
            "Cute cartoon character",
            "Vintage car on a city street"
        ]
        
        for suggestion in prompt_suggestions:
            if st.button(suggestion, key=f"suggest_{hash(suggestion)}", use_container_width=True):
                # Add suggestion to chat
                process_image_generation(gemini_client, suggestion, style, quality, aspect_ratio)
    
    with col1:
        # Chat interface
        st.subheader("💬 Conversation")
        
        # Display conversation history
        chat_container = st.container()
        with chat_container:
            for i, message in enumerate(st.session_state.gen_conversation):
                with st.chat_message(message["role"]):
                    st.write(message["content"])
        
        # Chat input
        user_input = st.chat_input(
            "Describe the image you want to create...",
            key="gen_chat_input"
        )
        
        if user_input:
            process_image_generation(gemini_client, user_input, style, quality, aspect_ratio)
        
        # Clear conversation button
        if st.session_state.gen_conversation:
            if st.button("🗑️ Clear Conversation", key="clear_gen_conv"):
                st.session_state.gen_conversation = []
                st.rerun()

def process_image_generation(gemini_client: GeminiClient, user_input: str, style: str, quality: str, aspect_ratio: str):
    """Process image generation request"""
    
    # Add user message to conversation
    st.session_state.gen_conversation.append({
        "role": "user", 
        "content": user_input
    })
    
    # Create enhanced prompt
    enhanced_prompt = create_enhanced_prompt(user_input, style, quality, aspect_ratio)
    
    # Generate with Gemini Flash
    with st.spinner("🎨 Generating image with Gemini Flash..."):
        try:
            response = gemini_client.generate_image(enhanced_prompt)
            
            if response:
                # Add successful response
                st.session_state.gen_conversation.append({
                    "role": "assistant",
                    "content": f"✅ Generated image concept for: '{user_input}'\n\n{response}"
                })
            else:
                st.session_state.gen_conversation.append({
                    "role": "assistant", 
                    "content": "❌ Sorry, image generation failed. Please try again with a different prompt."
                })
                
        except Exception as e:
            st.session_state.gen_conversation.append({
                "role": "assistant",
                "content": f"❌ Error generating image: {str(e)}"
            })
    
    st.rerun()

def create_enhanced_prompt(user_prompt: str, style: str, quality: str, aspect_ratio: str) -> str:
    """Create enhanced prompt with style and settings"""
    
    aspect_map = {
        "Square (1:1)": "square format, 1:1 aspect ratio",
        "Portrait (3:4)": "portrait orientation, 3:4 aspect ratio", 
        "Landscape (4:3)": "landscape orientation, 4:3 aspect ratio",
        "Wide (16:9)": "wide cinematic format, 16:9 aspect ratio"
    }
    
    quality_map = {
        "Standard": "good quality",
        "High Quality": "high resolution, detailed",
        "Professional": "professional quality, highly detailed, masterpiece"
    }
    
    enhanced = f"""
    Create a {style.lower()} style image: {user_prompt}
    
    Technical specifications:
    - Format: {aspect_map.get(aspect_ratio, 'square format')}
    - Quality: {quality_map.get(quality, 'high quality')}
    - Style: {style.lower()}
    
    Make it visually striking and professionally composed.
    """
    
    return enhanced.strip()
