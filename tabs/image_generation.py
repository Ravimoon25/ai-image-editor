import streamlit as st
from utils.gemini_client import GeminiClient
import io

def render():
    if not st.session_state.get('gemini_client'):
        st.warning("Configure API key first")
        return
    
    client = st.session_state.gemini_client
    
    st.header("Generate Images")
    
    # Simple prompt input
    prompt = st.text_area("Describe your image:", height=100)
    
    if st.button("Generate Image", type="primary") and prompt:
        with st.spinner("Generating..."):
            image = client.generate_image(prompt)
            
        if image:
            st.success("Image generated!")
            st.image(image, use_column_width=True)
            
            # Download button
            buf = io.BytesIO()
            image.save(buf, format='PNG')
            st.download_button(
                "Download Image",
                buf.getvalue(),
                "generated_image.png",
                "image/png"
            )
        else:
            st.error("Failed to generate image")
