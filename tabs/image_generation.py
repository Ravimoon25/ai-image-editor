import streamlit as st
from utils.gemini_client import GeminiClient
from utils.image_utils import ImageUtils
from utils.image_generator import ImageGenerator
from typing import Dict, List
import time

def render():
    """Render the Image Generation tab"""
    
    # Check if Gemini client is available
    if not st.session_state.get('gemini_client'):
        st.warning("⚠️ Please configure your Gemini API key in the sidebar first.")
        return
    
    gemini_client = st.session_state.gemini_client
    image_generator = ImageGenerator()
    
    # Initialize tab-specific session state
    if 'gen_conversation' not in st.session_state:
        st.session_state.gen_conversation = []
    if 'current_prompt' not in st.session_state:
        st.session_state.current_prompt = ""
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []
    
    st.markdown("### 🎨 Generate Images with AI")
    st.markdown("Describe the image you want to create!")
    
    # Two columns: chat and settings
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("⚙️ Generation Settings")
        
        # Image generation service selection
        gen_service = st.selectbox(
            "Generation Service",
            ["Hugging Face (Free)", "Conceptual (Gemini Only)", "Replicate API", "DALL-E API"],
            help="Choose how to generate images"
        )
        
        # API key inputs for different services
        hf_token = None
        if gen_service == "Hugging Face (Free)":
            st.info("💡 Hugging Face free tier - no API key required, but may be slower")
            hf_token = st.text_input(
                "HF Token (Optional)", 
                type="password",
                help="Hugging Face token for faster generation (optional)"
            )
            
        elif gen_service == "Replicate API":
            replicate_token = st.text_input("Replicate API Token", type="password")
            
        elif gen_service == "DALL-E API":
            openai_key = st.text_input("OpenAI API Key", type="password")
        
        # Style options
        style = st.selectbox(
            "Style",
            ["Photorealistic", "Digital Art", "Oil Painting", "Watercolor", "Sketch", "Cartoon", "Abstract"]
        )
        
        # Quick prompt suggestions
        st.divider()
        st.subheader("💡 Quick Ideas")
        prompt_suggestions = [
            "A serene mountain landscape at sunset",
            "Portrait of a person in professional attire", 
            "Abstract geometric patterns in vibrant colors",
            "A cozy coffee shop interior",
            "Futuristic city skyline",
            "Cute cartoon character",
            "Vintage car in a city street"
        ]
        
        for suggestion in prompt_suggestions:
            if st.button(suggestion, key=f"suggest_{hash(suggestion)}", use_container_width=True):
                st.session_state.current_prompt = suggestion
    
    with col1:
        # Chat interface
        st.subheader("💬 Conversation & Results")
        
        # Display conversation history and generated images
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
            
            # Enhanced prompt with style
            enhanced_prompt = enhance_prompt_with_gemini(gemini_client, user_input, style)
            
            if gen_service == "Hugging Face (Free)":
                # Generate actual image
                generated_image = image_generator.generate_with_huggingface(enhanced_prompt, hf_token)
                
                if generated_image:
                    # Add successful generation to conversation
                    st.session_state.gen_conversation.append({
                        "role": "assistant",
                        "content": f"✅ Generated image for: '{user_input}'\nEnhanced prompt: {enhanced_prompt}",
                        "image": generated_image
                    })
                    
                    # Store in generated images list
                    st.session_state.generated_images.append({
                        "prompt": user_input,
                        "enhanced_prompt": enhanced_prompt,
                        "image": generated_image,
                        "timestamp": time.time()
                    })
                else:
                    st.session_state.gen_conversation.append({
                        "role": "assistant",
                        "content": "❌ Sorry, image generation failed. Please try again with a different prompt or check your settings."
                    })
                    
            elif gen_service == "Conceptual (Gemini Only)":
                # Use Gemini for conceptual description only
                response = generate_conceptual_image(gemini_client, enhanced_prompt)
                st.session_state.gen_conversation.append({
                    "role": "assistant",
                    "content": response
                })
                
            else:
                # Placeholder for other services
                st.session_state.gen_conversation.append({
                    "role": "assistant",
                    "content": f"🚧 {gen_service} integration coming soon! For now, try 'Hugging Face (Free)' option."
                })
            
            st.rerun()
        
        # Generated images gallery
        if st.session_state.generated_images:
            st.divider()
            st.subheader("🖼️ Generated Images Gallery")
            
            # Display recent images in a grid
            cols = st.columns(3)
            for i, img_data in enumerate(reversed(st.session_state.generated_images[-6:])):  # Show last 6 images
                with cols[i % 3]:
                    st.image(img_data["image"], caption=f"'{img_data['prompt'][:30]}...", use_column_width=True)
                    
                    # Download button for each image
                    buffer = io.BytesIO()
                    img_data["image"].save(buffer, format="PNG")
                    buffer.seek(0)
                    
                    st.download_button(
                        label="📥",
                        data=buffer.getvalue(),
                        file_name=f"generated_{int(img_data['timestamp'])}.png",
                        mime="image/png",
                        key=f"download_gallery_{i}"
                    )
        
        # Clear conversation button
        if st.session_state.gen_conversation:
            col_clear1, col_clear2 = st.columns(2)
            with col_clear1:
                if st.button("🗑️ Clear Chat", key="clear_gen_conv"):
                    st.session_state.gen_conversation = []
                    st.rerun()
            with col_clear2:
                if st.button("🗑️ Clear Gallery", key="clear_gallery"):
                    st.session_state.generated_images = []
                    st.rerun()

def enhance_prompt_with_gemini(gemini_client: GeminiClient, user_prompt: str, style: str) -> str:
    """Use Gemini to enhance the user's prompt for better image generation"""
    
    enhancement_prompt = f"""
    Enhance this image generation prompt to be more descriptive and detailed for AI image generation:
    
    Original prompt: "{user_prompt}"
    Desired style: {style}
    
    Please provide a single, enhanced prompt (maximum 100 words) that includes:
    - More specific visual details
    - Better composition description  
    - Appropriate style elements
    - Technical photography terms if relevant
    
    Return ONLY the enhanced prompt, nothing else.
    """
    
    try:
        if not gemini_client.chat:
            gemini_client.start_conversation()
        
        enhanced = gemini_client.send_message(enhancement_prompt)
        # Clean up the response to get just the prompt
        enhanced = enhanced.strip().replace('"', '').replace('\n', ' ')
        return enhanced[:200]  # Limit length
        
    except Exception as e:
        # Fallback to original prompt with style
        return f"{user_prompt}, {style.lower()} style"

def generate_conceptual_image(gemini_client: GeminiClient, prompt: str) -> str:
    """Generate conceptual image description using Gemini"""
    
    system_prompt = """
    You are an expert image generation assistant. Provide a detailed creative description 
    and technical guidance for the image concept. Include composition, lighting, colors, 
    and artistic elements.
    """
    
    try:
        if not gemini_client.chat:
            gemini_client.start_conversation()
        
        full_prompt = f"{system_prompt}\n\nImage concept: {prompt}"
        response = gemini_client.send_message(full_prompt)
        return response
        
    except Exception as e:
        return "Sorry, I encountered an error while processing your image generation request."
