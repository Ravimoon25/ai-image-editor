import streamlit as st
from utils.gemini_client import GeminiClient
from utils.image_utils import ImageUtils
from typing import Dict, List
import requests
from PIL import Image
import io

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
    if 'current_prompt' not in st.session_state:
        st.session_state.current_prompt = ""
    
    st.markdown("### 🎨 Generate Images with AI")
    st.markdown("Describe the image you want to create, and I'll help you generate it!")
    
    # Two columns: chat and settings
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("⚙️ Generation Settings")
        
        # Image generation service selection
        gen_service = st.selectbox(
            "Generation Service",
            ["Conceptual (Gemini Guided)", "External API"],
            help="Choose how to generate images"
        )
        
        if gen_service == "External API":
            st.info("💡 For actual image generation, you'll need to integrate with services like:\n- DALL-E API\n- Stable Diffusion API\n- Midjourney API")
        
        # Style options
        style = st.selectbox(
            "Style",
            ["Photorealistic", "Digital Art", "Oil Painting", "Watercolor", "Sketch", "Cartoon", "Abstract"]
        )
        
        # Aspect ratio
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            ["Square (1:1)", "Portrait (3:4)", "Landscape (4:3)", "Wide (16:9)"]
        )
        
        # Quality settings
        quality = st.slider("Quality", 1, 10, 7)
        
        st.divider()
        
        # Quick prompt suggestions
        st.subheader("💡 Quick Ideas")
        prompt_suggestions = [
            "A serene mountain landscape at sunset",
            "Portrait of a person in professional attire",
            "Abstract geometric patterns in vibrant colors",
            "A cozy coffee shop interior",
            "Futuristic city skyline"
        ]
        
        for suggestion in prompt_suggestions:
            if st.button(suggestion, key=f"suggest_{hash(suggestion)}", use_container_width=True):
                st.session_state.current_prompt = suggestion
    
    with col1:
        # Chat interface
        st.subheader("💬 Conversation")
        
        # Display conversation history
        chat_container = st.container()
        with chat_container:
            for i, message in enumerate(st.session_state.gen_conversation):
                with st.chat_message(message["role"]):
                    st.write(message["content"])
                    if "image" in message:
                        ImageUtils.display_image_with_download(
                            message["image"], 
                            caption="Generated Image",
                            key=f"gen_{i}"
                        )
        
        # Chat input
        user_input = st.chat_input(
            "Describe the image you want to create...",
            key="gen_chat_input"
        )
        
        # Use suggested prompt if available
        if st.session_state.current_prompt and not user_input:
            user_input = st.session_state.current_prompt
            st.session_state.current_prompt = ""
        
        if user_input:
            # Add user message to conversation
            st.session_state.gen_conversation.append({
                "role": "user", 
                "content": user_input
            })
            
            # Process with Gemini
            with st.spinner("🎨 Creating your image..."):
                # Enhanced prompt with style and settings
                enhanced_prompt = create_enhanced_prompt(user_input, style, aspect_ratio, quality)
                
                if gen_service == "Conceptual (Gemini Guided)":
                    # Use Gemini to create a detailed description and guidance
                    response = generate_conceptual_image(gemini_client, enhanced_prompt)
                else:
                    # Placeholder for external API integration
                    response = "External API integration needed for actual image generation."
                
                # Add AI response to conversation
                st.session_state.gen_conversation.append({
                    "role": "assistant",
                    "content": response
                })
            
            st.rerun()
        
        # Clear conversation button
        if st.session_state.gen_conversation:
            if st.button("🗑️ Clear Conversation", key="clear_gen_conv"):
                st.session_state.gen_conversation = []
                st.rerun()

def create_enhanced_prompt(user_prompt: str, style: str, aspect_ratio: str, quality: int) -> str:
    """Create an enhanced prompt with style and technical parameters"""
    
    aspect_map = {
        "Square (1:1)": "square format",
        "Portrait (3:4)": "portrait orientation",
        "Landscape (4:3)": "landscape orientation", 
        "Wide (16:9)": "wide cinematic format"
    }
    
    quality_map = {
        1: "draft quality",
        2: "low quality", 
        3: "basic quality",
        4: "good quality",
        5: "standard quality",
        6: "high quality",
        7: "very high quality",
        8: "premium quality", 
        9: "professional quality",
        10: "masterpiece quality"
    }
    
    enhanced = f"""
    Create an image with the following specifications:
    
    Content: {user_prompt}
    Style: {style.lower()}
    Format: {aspect_map.get(aspect_ratio, 'square format')}
    Quality: {quality_map.get(quality, 'high quality')}
    
    Please provide detailed creative direction and technical specifications for this image.
    """
    
    return enhanced

def generate_conceptual_image(gemini_client: GeminiClient, prompt: str) -> str:
    """Generate conceptual image description using Gemini"""
    
    system_prompt = """
    You are an expert image generation assistant. When a user describes an image they want to create, 
    provide:
    
    1. A detailed, enhanced description of the image
    2. Technical specifications (composition, lighting, colors)
    3. Style guidance
    4. Suggestions for improvement or variations
    
    Be creative and detailed in your descriptions. Since actual image generation requires external APIs, 
    focus on providing comprehensive creative direction.
    """
    
    try:
        # Start conversation if not already started
        if not gemini_client.chat:
            gemini_client.start_conversation()
        
        full_prompt = f"{system_prompt}\n\nUser request: {prompt}"
        response = gemini_client.send_message(full_prompt)
        
        return response
        
    except Exception as e:
        st.error(f"Error generating image concept: {str(e)}")
        return "Sorry, I encountered an error while processing your image generation request."
