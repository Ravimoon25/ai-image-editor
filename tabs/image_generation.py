import streamlit as st
from utils.gemini_client import GeminiClient
from utils.image_utils import ImageUtils
import time

def render():
    if not st.session_state.get('gemini_client'):
        st.warning("Configure API key first")
        return
    
    gemini_client = st.session_state.gemini_client
    
    if 'gen_conversation' not in st.session_state:
        st.session_state.gen_conversation = []
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []
    
    st.markdown("### 🎨 Generate Images with Imagen 4.0")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("⚙️ Settings")
        
        # Style options
        style = st.selectbox(
            "Style",
            ["Photorealistic", "Digital Art", "Oil Painting", "Watercolor", "Cartoon", "Abstract"]
        )
        
        # Quick suggestions
        st.subheader("💡 Quick Ideas")
        suggestions = [
            "A serene mountain landscape",
            "Portrait of a professional person",
            "Abstract colorful artwork",
            "Cozy coffee shop interior",
            "Futuristic city skyline"
        ]
        
        for suggestion in suggestions:
            if st.button(suggestion, key=f"sug_{hash(suggestion)}", use_container_width=True):
                generate_image_with_prompt(gemini_client, suggestion, style)
    
    with col1:
        # Simple prompt input
        user_input = st.text_area(
            "Describe your image:",
            placeholder="A beautiful sunset over mountains",
            height=100
        )
        
        if st.button("🎨 Generate Image", type="primary") and user_input:
            generate_image_with_prompt(gemini_client, user_input, style)
        
        # Show conversation and images
        for i, msg in enumerate(st.session_state.gen_conversation):
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if "image" in msg:
                    ImageUtils.display_image_with_download(
                        msg["image"], 
                        caption="Generated Image",
                        key=f"img_{i}"
                    )
        
        if st.button("🗑️ Clear All"):
            st.session_state.gen_conversation = []
            st.session_state.generated_images = []
            st.rerun()

def generate_image_with_prompt(gemini_client: GeminiClient, prompt: str, style: str):
    """Generate image with the given prompt"""
    
    # Add user message
    st.session_state.gen_conversation.append({
        "role": "user", 
        "content": prompt
    })
    
    # Enhanced prompt with style
    enhanced_prompt = f"{prompt}, {style.lower()} style"
    
    with st.spinner("🎨 Generating image with Imagen 4.0..."):
        # Generate actual image
        image = gemini_client.generate_image(enhanced_prompt)
        
        if image:
            # Success - add image to conversation
            st.session_state.gen_conversation.append({
                "role": "assistant",
                "content": f"✅ Generated: {prompt}",
                "image": image
            })
            
            # Store in gallery
            st.session_state.generated_images.append({
                "prompt": prompt,
                "image": image,
                "timestamp": time.time()
            })
            
        else:
            # Failed
            st.session_state.gen_conversation.append({
                "role": "assistant",
                "content": f"❌ Failed to generate image for: {prompt}"
            })
    
    st.rerun()
