# Configuration file for AI Image Studio Pro
import streamlit as st
from google import genai
from google.genai import types

# Model configuration
MODEL_ID = "gemini-2.5-flash-image-preview"

# Style and content options
STYLE_PRESETS = {
    "Photorealistic": "ultra-realistic, high-definition, professional photography, sharp details",
    "Digital Art": "digital painting, concept art, detailed illustration, vibrant colors",
    "Cartoon Style": "cartoon, animated style, colorful and fun, playful",
    "Oil Painting": "classical oil painting, artistic brushstrokes, textured canvas",
    "Sketch": "pencil sketch, hand-drawn, artistic lines, monochrome",
    "Vintage": "vintage style, retro aesthetic, aged look, nostalgic",
    "Cyberpunk": "neon lights, futuristic, cyberpunk aesthetic, dark atmosphere",
    "Minimalist": "clean, simple, minimalist design, elegant simplicity"
}

ASPECT_RATIOS = {
    "Square (1:1)": "square format, equal dimensions",
    "Portrait (3:4)": "portrait orientation, vertical composition",
    "Landscape (4:3)": "landscape orientation, horizontal composition", 
    "Wide (16:9)": "wide format, cinematic composition"
}

CLOTHING_OPTIONS = {
    "Business Formal": "professional business suit, formal corporate attire, executive styling",
    "Casual Wear": "comfortable jeans and t-shirt, relaxed everyday clothing",
    "Elegant Evening": "sophisticated evening dress, formal party attire, glamorous",
    "Traditional Indian": "beautiful traditional Indian clothing, saree, kurta, cultural dress",
    "Wedding Attire": "elegant wedding dress, formal wedding suit, bridal styling",
    "Sportswear": "athletic wear, gym clothes, sports uniform, active lifestyle",
    "Winter Wear": "warm winter coat, cozy sweater, seasonal layered clothing",
    "Beach Wear": "summer beach outfit, light breezy clothing, vacation style",
    "Vintage Style": "retro vintage clothing from past decades, classic fashion",
    "Designer Fashion": "high-end designer clothing, luxury fashion, couture styling"
}

POSE_OPTIONS = {
    "Confident Standing": "confident upright posture, hands on hips, strong authoritative stance",
    "Relaxed Casual": "relaxed natural pose, comfortable casual body language",
    "Professional Portrait": "professional headshot pose, business appropriate, executive presence",
    "Dynamic Action": "energetic dynamic pose, movement and life, active positioning",
    "Sitting Elegant": "graceful sitting position, elegant refined posture",
    "Walking Forward": "confident walking stride, forward motion, purposeful movement",
    "Arms Crossed": "confident pose with arms crossed, assertive professional stance",
    "Waving Hello": "friendly waving gesture, welcoming approachable pose",
    "Thinking Pose": "thoughtful pose, hand on chin, contemplative positioning",
    "Victory Pose": "celebratory victory stance, arms raised, triumphant gesture"
}

FACIAL_EXPRESSIONS = {
    "Natural Smile": "genuine natural smile, warm and friendly expression",
    "Confident Look": "confident serious expression, professional authoritative demeanor", 
    "Joyful Laugh": "happy laughing expression, pure joy and happiness",
    "Thoughtful": "contemplative thoughtful expression, intelligent focused look",
    "Surprised": "surprised expression, wide eyes, astonished look",
    "Peaceful": "calm peaceful expression, serene tranquil look"
}

BACKGROUND_OPTIONS = {
    "Smart Remove": "completely remove background, create transparent PNG",
    "Studio Professional": "professional studio lighting, clean neutral backdrop",
    "Modern Office": "contemporary office environment, professional workspace",
    "Outdoor Natural": "beautiful outdoor natural setting, parks or landscapes",
    "Urban City": "modern city environment, urban professional setting",
    "Home Lifestyle": "cozy home interior, comfortable living space",
    "Product Studio": "e-commerce white background, clean product photography",
    "Fantasy World": "magical fantasy environment, creative artistic backdrop",
    "Seasonal Theme": "seasonal environment, holiday or weather-themed backdrop"
}

FACE_ENHANCEMENT = {
    "Skin Perfection": "smooth flawless skin, remove blemishes naturally, even skin tone",
    "Eye Enhancement": "brighter sparkling eyes, natural eye enhancement", 
    "Smile Improvement": "perfect natural smile, teeth whitening, confident expression",
    "Hair Styling": "perfect hairstyle, natural hair enhancement, styled look",
    "Overall Beauty": "natural beauty enhancement, subtle professional improvement",
    "Age Adjustment": "youthful appearance, age-appropriate enhancement"
}

BODY_MODIFICATIONS = {
    "Fitness Transform": "athletic toned body, fit healthy appearance, natural muscle definition",
    "Posture Improvement": "confident straight posture, professional body language",
    "Height Enhancement": "taller proportional appearance, elegant stature",
    "Body Proportions": "balanced natural body proportions, harmonious physique",
    "Clothing Fit": "perfectly fitted clothing, tailored professional appearance"
}

@st.cache_resource
def get_client():
    """Initialize Gemini client with error handling"""
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize AI client: {str(e)}")
        st.stop()
