import streamlit as st
from utils.gemini_client import GeminiClient

def render():
    if not st.session_state.get('gemini_client'):
        st.warning("Configure API key first")
        return
    
    gemini_client = st.session_state.gemini_client
    
    if 'gen_conversation' not in st.session_state:
        st.session_state.gen_conversation = []
    
    st.markdown("### 🎨 Generate Images with Gemini 2.5 Flash")
    
    # Simple prompt input
    user_input = st.text_area(
        "Describe your image:",
        placeholder="A beautiful sunset over mountains",
        height=100
    )
    
    if st.button("🎨 Generate", type="primary") and user_input:
        st.session_state.gen_conversation.append({"role": "user", "content": user_input})
        
        with st.spinner("Generating..."):
            prompt = f"Create a detailed description for this image: {user_input}"
            response = gemini_client.generate_content(prompt)
            
        st.session_state.gen_conversation.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Show conversation
    for msg in st.session_state.gen_conversation:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if st.button("Clear"):
        st.session_state.gen_conversation = []
        st.rerun()
