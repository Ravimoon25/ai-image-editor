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
            ["Photorealistic", "Digital Art", "Oil Painting", "Watercolor", "Sketch", "Cartoon", "Abstract"],
            index=0
        )
        
        # Quality settings
        quality = st.selectbox(
            "Quality",
            ["Standard", "High Quality", "Professional"],
            index=1
        )
        
        # Aspect ratio
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            ["Square (1:1)", "Portrait (3:4)", "Landscape (4:3)", "Wide (16:9)"],
            index=0
        )
        
        st.divider()
        
        # Quick prompt suggestions
        st.subheader("💡 Quick Ideas")
        st.markdown("*Click any button to generate:*")
        
        prompt_suggestions = [
            "A serene mountain landscape at sunset",
            "Portrait of a professional person",
            "Abstract geometric art with vibrant colors", 
            "A cozy coffee shop interior",
            "Futuristic city skyline",
            "Cute cartoon character",
            "Vintage car on a city street",
            "Space exploration scene",
            "Tropical beach paradise",
            "Medieval castle in fog"
        ]
        
        for i, suggestion in enumerate(prompt_suggestions):
            if st.button(
                suggestion, 
                key=f"suggest_{i}", 
                use_container_width=True,
                help=f"Generate: {suggestion}"
            ):
                # Add suggestion as user message and process
                st.session_state.gen_conversation.append({
                    "role": "user", 
                    "content": suggestion
                })
                process_image_generation_async(gemini_client, suggestion, style, quality, aspect_ratio)
                st.rerun()
    
    with col1:
        st.subheader("💬 Generate Images")
        
        # Prompt input form - MAIN INTERFACE
        with st.form(key="image_prompt_form", clear_on_submit=True):
            st.markdown("**Enter your image description:**")
            
            # Text area for longer prompts
            user_prompt = st.text_area(
                "",
                placeholder="Describe the image you want to create...\n\nExample: 'A beautiful sunset over mountains with purple clouds'",
                height=100,
                key="prompt_input"
            )
            
            # Form columns for submit and clear
            col_submit, col_clear = st.columns([1, 1])
            
            with col_submit:
                submitted = st.form_submit_button(
                    "🎨 Generate Image", 
                    use_container_width=True,
                    type="primary"
                )
            
            with col_clear:
                if st.form_submit_button(
                    "🗑️ Clear Chat", 
                    use_container_width=True
                ):
                    st.session_state.gen_conversation = []
                    st.rerun()
        
        # Process form submission
        if submitted and user_prompt.strip():
            # Add user message to conversation
            st.session_state.gen_conversation.append({
                "role": "user", 
                "content": user_prompt.strip()
            })
            
            process_image_generation_async(gemini_client, user_prompt.strip(), style, quality, aspect_ratio)
            st.rerun()
        elif submitted and not user_prompt.strip():
            st.warning("Please enter a description for your image!")
        
        # Display conversation history
        st.divider()
        st.subheader("💭 Generation History")
        
        if st.session_state.gen_conversation:
            # Chat container with fixed height
            chat_container = st.container(height=400)
            with chat_container:
                for i, message in enumerate(st.session_state.gen_conversation):
                    with st.chat_message(message["role"]):
                        st.write(message["content"])
                        
                        # Add copy button for AI responses
                        if message["role"] == "assistant" and len(message["content"]) > 50:
                            st.button(
                                "📋 Copy Response", 
                                key=f"copy_{i}",
                                help="Copy this response to clipboard"
                            )
        else:
            st.info("🎨 No images generated yet. Enter a prompt above to get started!")
        
        # Statistics
        if st.session_state.gen_conversation:
            user_messages = [msg for msg in st.session_state.gen_conversation if msg["role"] == "user"]
            st.caption(f"📊 Total prompts submitted: {len(user_messages)}")

def process_image_generation_async(gemini_client: GeminiClient, user_input: str, style: str, quality: str, aspect_ratio: str):
    """Process image generation request with loading state"""
    
    # Create enhanced prompt
    enhanced_prompt = create_enhanced_prompt(user_input, style, quality, aspect_ratio)
    
    # Show processing status
    status_placeholder = st.empty()
    
    with status_placeholder:
        with st.status("🎨 Generating with Gemini Flash...", expanded=True) as status:
            st.write("📝 Enhancing your prompt...")
            st.write(f"🎯 Style: {style}")
            st.write(f"⚡ Quality: {quality}")
            st.write(f"📐 Format: {aspect_ratio}")
            
            try:
                # Generate with Gemini Flash
                st.write("🤖 Sending to Gemini...")
                response = gemini_client.generate_image(enhanced_prompt)
                
                if response:
                    status.update(label="✅ Generation completed!", state="complete")
                    
                    # Add successful response
                    st.session_state.gen_conversation.append({
                        "role": "assistant",
                        "content": f"✅ **Generated image concept for:** *'{user_input}'*\n\n**Enhanced prompt used:**\n{enhanced_prompt}\n\n**Result:**\n{response}"
                    })
                else:
                    status.update(label="❌ Generation failed", state="error")
                    st.session_state.gen_conversation.append({
                        "role": "assistant", 
                        "content": "❌ Sorry, image generation failed. Please try again with a different prompt."
                    })
                    
            except Exception as e:
                status.update(label="❌ Error occurred", state="error")
                st.session_state.gen_conversation.append({
                    "role": "assistant",
                    "content": f"❌ **Error generating image:** {str(e)}\n\nPlease try again with a different prompt."
                })
    
    # Clear the status after processing
    status_placeholder.empty()

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
    
    enhanced = f"""Create a {style.lower()} style image: {user_prompt}

Technical specifications:
- Format: {aspect_map.get(aspect_ratio, 'square format')}
- Quality: {quality_map.get(quality, 'high quality')}
- Style: {style.lower()}

Make it visually striking and professionally composed."""
    
    return enhanced.strip()
