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
if 'current_api_key' not in st.session_state:
    st.session_state.current_api_key = None

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
        api_key = api_key_from_secrets
        
        # Auto-initialize client if not done
        if not st.session_state.get('gemini_client'):
            try:
                st.session_state['gemini_api_key'] = api_key
                st.session_state['current_api_key'] = api_key
                st.session_state.gemini_client = GeminiClient(api_key)
                st.success("✅ Gemini client auto-initialized!")
            except Exception as e:
                st.error(f"❌ Failed to initialize client: {e}")
                st.info("Please check your API key in secrets")
        
        # Optional: Allow override
        with st.expander("🔧 Override API Key (Optional)"):
            manual_key = st.text_input(
                "Manual API Key", 
                type="password", 
                help="Override the secrets API key if needed"
            )
            if manual_key and Settings.validate_api_key(manual_key):
                if st.button("Use Override Key"):
                    try:
                        api_key = manual_key
                        st.session_state['gemini_api_key'] = api_key
                        st.session_state['current_api_key'] = api_key
                        st.session_state.gemini_client = GeminiClient(api_key)
                        st.success("✅ Using manual override key!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to use override key: {e}")
    else:
        # Show manual input if no secrets
        st.warning("⚠️ No API key found in secrets")
        st.info("Please add GEMINI_API_KEY to your Streamlit secrets or enter manually below:")
        
        api_key = st.text_input(
            "Gemini API Key", 
            type="password", 
            help="Enter your Gemini API key from Google AI Studio",
            placeholder="AIza..."
        )
        
        if api_key:
            if Settings.validate_api_key(api_key):
                if st.button("🔗 Connect to Gemini", type="primary"):
                    try:
                        with st.spinner("Connecting to Gemini..."):
                            st.session_state['gemini_api_key'] = api_key
                            st.session_state['current_api_key'] = api_key
                            st.session_state.gemini_client = GeminiClient(api_key)
                            st.success("✅ Connected successfully!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Connection failed: {e}")
                        st.info("Please check your API key")
            else:
                st.error("❌ Invalid API key format. Should start with 'AIza'")
        else:
            st.info("👆 Enter your API key above to get started")
    
    # Connection status indicator
    st.divider()
    if st.session_state.get('gemini_client'):
        st.success("🤖 **Gemini Client Ready**")
        
        # Test connection button
        if st.button("🔍 Test Connection"):
            try:
                with st.spinner("Testing..."):
                    test_result = GeminiClient.validate_connection(st.session_state.current_api_key)
                    if test_result:
                        st.success("✅ Connection test passed!")
                    else:
                        st.error("❌ Connection test failed")
            except Exception as e:
                st.error(f"Test failed: {e}")
        
        # Reset connection button
        if st.button("🔄 Reset Connection"):
            st.session_state.gemini_client = None
            st.session_state.current_api_key = None
            st.rerun()
    else:
        st.error("❌ **Gemini Client Not Ready**")
        st.info("Configure API key above to enable all features")
    
    # Additional settings
    st.divider()
    st.subheader("📋 App Settings")
    st.info(f"📏 Max image size: {Settings.MAX_IMAGE_SIZE // (1024*1024)}MB")
    st.info(f"🗂️ Supported formats: {', '.join(Settings.SUPPORTED_FORMATS)}")
    
    # Debug info (expandable)
    with st.expander("🔧 Debug Info"):
        st.write("Session State:")
        st.write(f"- Has client: {bool(st.session_state.get('gemini_client'))}")
        st.write(f"- API key set: {bool(st.session_state.get('current_api_key'))}")
        st.write(f"- Secrets available: {Settings.has_api_key_in_secrets()}")

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
    if api_ready:
        image_generation.render()
    else:
        st.warning("⚠️ Please configure your Gemini API key in the sidebar first.")
        st.info("Once connected, you'll be able to generate images with AI!")
        
        # Show preview of what's coming
        st.markdown("### 🎨 Image Generation Features:")
        st.markdown("""
        - **Natural Language Prompts**: Describe images in plain English
        - **Style Controls**: Choose from photorealistic, artistic, cartoon styles
        - **Quality Settings**: Standard to professional quality
        - **Aspect Ratios**: Square, portrait, landscape, wide formats
        - **Quick Ideas**: Pre-made prompts to get started
        - **Conversation History**: Track all your generations
        """)

with tab2:
    st.header("✏️ General Image Editing")
    if api_ready:
        st.info("🚧 Image editing features coming soon!")
        st.markdown("### Planned Features:")
        st.markdown("""
        - **Background Replacement**: Change backgrounds with AI
        - **Object Removal**: Remove unwanted elements
        - **Object Addition**: Add new elements to images
        - **Style Transfer**: Apply artistic styles
        - **Smart Cropping**: AI-powered composition
        """)
    else:
        st.warning("⚠️ Please configure your Gemini API key in the sidebar first.")

with tab3:
    st.header("👤 Face & Body Modification")
    if api_ready:
        st.info("🚧 Face & body editing features coming soon!")
        st.markdown("### Planned Features:")
        st.markdown("""
        - **Facial Expression Changes**: Modify emotions and expressions
        - **Body Type Adjustments**: Change body proportions
        - **Age Progression/Regression**: Make subjects older or younger
        - **Style Changes**: Modify appearance while preserving identity
        - **Professional Retouching**: AI-powered enhancement
        """)
    else:
        st.warning("⚠️ Please configure your Gemini API key in the sidebar first.")

with tab4:
    st.header("📸 Professional Headshots")
    if api_ready:
        st.info("🚧 Headshot generation features coming soon!")
        st.markdown("### Planned Features:")
        st.markdown("""
        - **Professional Styling**: Convert casual photos to professional headshots
        - **Background Options**: Studio, office, or custom backgrounds
        - **Lighting Enhancement**: Professional portrait lighting
        - **Clothing Suggestions**: Professional attire recommendations
        - **Multiple Variations**: Generate different styles from one photo
        """)
    else:
        st.warning("⚠️ Please configure your Gemini API key in the sidebar first.")

# Footer
st.divider()
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("**Built with ❤️ using:**")
    st.markdown("- Streamlit")
    st.markdown("- Gemini AI")

with col_footer2:
    if api_ready:
        st.metric("Status", "🟢 Connected", "Ready")
    else:
        st.metric("Status", "🔴 Disconnected", "Setup needed")

with col_footer3:
    st.markdown("**Quick Actions:**")
    if not api_ready:
        st.markdown("1. Add API key in sidebar")
        st.markdown("2. Click 'Connect to Gemini'")
        st.markdown("3. Start generating images!")
    else:
        st.markdown("✅ Ready to use all features!")
