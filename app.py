
import streamlit as st
from config.settings import Settings
from utils.gemini_client import GeminiClient
from tabs import image_generation
# Page configuration
st.set_page_config(
    page_title="AI Image Editor",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'gemini_client' not in st.session_state:
    st.session_state.gemini_client = None
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# App title
st.title("🎨 AI Image Editor with Gemini")
st.markdown("Transform your images with conversational AI editing")

# Sidebar for API key and settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Check if API key is in secrets
    api_key_from_secrets = Settings.get_gemini_api_key()
    
    if Settings.has_api_key_in_secrets():
        st.success("🔑 API Key loaded from secrets")
        st.info("Using configured API key from Streamlit secrets")
        api_key = api_key_from_secrets
        
        # Optional: Allow override
        with st.expander("Override API Key (Optional)"):
            manual_key = st.text_input(
                "Manual API Key", 
                type="password", 
                help="Override the secrets API key if needed"
            )
            if manual_key and Settings.validate_api_key(manual_key):
                api_key = manual_key
                st.warning("Using manual override key")
    else:
        # Show manual input if no secrets
        st.warning("No API key found in secrets")
        api_key = st.text_input(
            "Gemini API Key", 
            type="password", 
            help="Enter your Gemini API key from Google AI Studio"
        )
    
    if api_key:
        if Settings.validate_api_key(api_key):
            # Test connection button (only show if not already connected)
            if not st.session_state.get('gemini_client') or st.session_state.get('current_api_key') != api_key:
                if st.button("Test Connection"):
                    with st.spinner("Testing connection..."):
                        if GeminiClient.validate_connection(api_key):
                            st.success("✅ Connected successfully!")
                            st.session_state['gemini_api_key'] = api_key
                            st.session_state['current_api_key'] = api_key
                            st.session_state.gemini_client = GeminiClient(api_key)
                        else:
                            st.error("❌ Failed to connect. Please check your API key.")
            else:
                st.success("✅ API Key configured and connected!")
                # Auto-initialize client if not done
                if not st.session_state.get('gemini_client'):
                    st.session_state['gemini_api_key'] = api_key
                    st.session_state['current_api_key'] = api_key
                    st.session_state.gemini_client = GeminiClient(api_key)
        else:
            st.error("Invalid API key format")
    else:
        st.warning("Please configure your Gemini API key")
    
    # Additional settings
    st.divider()
    st.subheader("App Settings")
    st.info(f"Max image size: {Settings.MAX_IMAGE_SIZE // (1024*1024)}MB")
    st.info(f"Supported formats: {', '.join(Settings.SUPPORTED_FORMATS)}")


# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🖼️ Generate Images", 
    "✏️ Edit Images", 
    "👤 Face & Body", 
    "📸 Headshot Studio"
])

# Check if API is configured before showing tab content
api_ready = st.session_state.get('gemini_client') is not None

with tab1:
    image_generation.render()

with tab2:
    st.header("General Image Editing")
    if api_ready:
        st.write("Ready to edit images!")
    else:
        st.warning("Please configure your Gemini API key in the sidebar first.")

with tab3:
    st.header("Face & Body Modification")
    if api_ready:
        st.write("Ready for face and body editing!")
    else:
        st.warning("Please configure your Gemini API key in the sidebar first.")

with tab4:
    st.header("Professional Headshots")
    if api_ready:
        st.write("Ready to create professional headshots!")
    else:
        st.warning("Please configure your Gemini API key in the sidebar first.")

# Footer
st.divider()
st.markdown("Built with ❤️ using Streamlit and Gemini AI")
