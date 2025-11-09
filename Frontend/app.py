import streamlit as st
import base64
import os
from sidebar import load_sidebar  # ✅ Import reusable sidebar
from contextlib import suppress # To handle conditional imports gracefully

# --- Page Config ---
st.set_page_config(page_title="Health IQ", layout="wide")

# --- Load Sidebar (Creates the custom navigation you want to keep) ---
# NOTE: This function creates the 'Navigation' links manually.
load_sidebar()

# --- Encode images as base64 safely ---
def get_base64(file):
    if not os.path.exists(file):
        # Handle missing file gracefully, important for background images
        return ""
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- Paths ---
BASE_DIR = os.path.dirname(__file__)
bg_path = os.path.join(BASE_DIR, "background.jpeg")

# --- Encoded Background Image ---
bg_img = get_base64(bg_path)

# --- Custom CSS (Hides the duplicate page list and applies styling) ---
st.markdown(f"""
<style>
/* 🚨 FIX: HIDES THE AUTOMATIC PAGE LIST IN THE SIDEBAR */
/* This targets the container that holds the auto-generated Streamlit page links */
div[data-testid="stSidebarNav"] {{
    display: none;
}}

/* --- Optional: Hides the 'Connecting' / Main Menu --- */
#MainMenu, header {{
    visibility: hidden;
}}


.stApp {{
    font-family: "Arial", sans-serif;
    background: url("data:image/jpeg;base64,{bg_img}") no-repeat center center fixed;
    background-size: cover;
    color: #1f4e79;
}}
.hero {{
    text-align: center;
    margin-top: -50px;
    margin-bottom: 50px;
}}
.hero h1 {{
    font-size: 50px;
    font-weight: 900;
    background: linear-gradient(135deg, #00FF00, #0000FF, #800080);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.hero p {{
    font-size: 22px;
    color: #1f4e79;
    margin-top: 10px;
}}
.emoji-box {{
    background: white;
    display: inline-block;
    padding: 20px 30px;
    border-radius: 40px;
    margin-top: 20px;
    font-size: 28px;
    box-shadow: 0 0 30px 2px #00FF00;
}}
.cta-box {{
    background: white;
    padding: 25px;
    border-radius: 15px;
    max-width: 600px;
    margin: 1px auto 40px auto;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}}
.cta-box h2 {{
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    color: #1f4e79;
}}
.cta-box p {{
    text-align: center;
    margin-top: 12px;
    font-size: 18px;
    color: #444;
}}

/* Gradient button for Streamlit button */
div.stButton > button:first-child {{
    background: linear-gradient(135deg, #00FF00, #0000FF);
    color: white;
    font-size: 22px;
    font-weight: 700;
    padding: 15px 40px;
    border-radius: 15px;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}}
div.stButton > button:first-child:hover {{
    background: linear-gradient(135deg, #00CC00, #0000CC);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}}
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero">
    <h1>AI Health Monitoring System</h1>
    <p>Detect your mood and get personalized recommendations for better well-being.</p>
    <div class="emoji-box">😊 😔 😴 😲 🤔</div>
</div>
""", unsafe_allow_html=True)

# --- CTA Section ---
st.markdown("""
<div class="cta-box">
    <h2>Get Started Today</h2>
    <p>Begin your journey to better mental health with our AI-powered mood detection and wellness recommendations.</p>
</div>
""", unsafe_allow_html=True)

# --- Centered Streamlit button with gradient (page switch works) ---
col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("🚀 Start Mood Analysis", use_container_width=True):
        # NOTE: Using suppress here is a minor cleanup, assuming you use st.switch_page
        with suppress(Exception):
            st.switch_page("Pages/Signup.py")