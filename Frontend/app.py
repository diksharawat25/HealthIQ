import streamlit as st
import base64
import os

st.set_page_config(page_title="MoodCare AI", layout="wide")

# --- Encode images as base64 ---
def get_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Background and logo
BASE_DIR = os.path.dirname(__file__)
img_path = os.path.join(BASE_DIR, "background.jpeg")
logo_path = os.path.join(BASE_DIR, "logo.png")

img_base64 = get_base64(img_path)
logo_base64 = get_base64(logo_path)
# --- Custom CSS ---
st.markdown(f"""
<style>
.stApp {{
    font-family: "Arial", sans-serif;
    background: url("data:image/jpeg;base64,{img_base64}") no-repeat center center fixed;
    background-size: cover;
}}
/* Top Navbar */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 15px 50px;
    width: 100%;
    border-radius: 0px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    position: fixed;
    top: 60px;
    left: 0;
    z-index: 1000;
}}
.navbar-left {{
    display: flex;
    align-items: center;
}}
.navbar-left img {{
    width: 120px;
    height: auto;
    margin-right: 10px;
    border-radius: 0px;
}}
.navbar-center a {{
    margin: 0 15px;
    text-decoration: none;
    font-size: 20px;
    color: #333;
    font-weight: 600;
}}
.navbar-center a:hover {{
    color: #2e77d0;
}}
.navbar-right a {{
    margin-left: 20px;
    font-size: 18px;
    font-weight: bold;
    text-decoration: none;
    padding: 12px 25px;
    border-radius: 25px;
    border: 2px solid #2e77d0;
}}
.login-btn {{
    color: #2e77d0;
    background: white;
}}
.login-btn:hover {{
    background: #f0f0f0;
}}
.signup-btn {{
    background: linear-gradient(90deg, #04AA6D, #2e77d0);
    color: white !important;  
    border: none;
}}
.signup-btn:hover {{
    opacity: 0.9;
    color: white !important; 
}}
/* Hero Section */
.hero {{
    text-align: center;
    margin-top: 80px;
    margin-bottom: 50px;
}}
.hero h1 {{
    font-size: 60px;
    font-weight: 900;
    background: linear-gradient(90deg, #04AA6D, #2e77d0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.hero p {{
    font-size: 24px;
    color: #333;
    margin-top: 15px;
}}
.emoji-box {{
    background: white;
    display: inline-block;
    padding: 20px 30px;
    border-radius: 40px;
    margin-top: 25px;
    font-size: 28px;
    /* Green outer glow */
    box-shadow: 0 0 20px 5px rgba(0, 200, 0, 0.6);
}}
/* Get Started Section */
.cta-box {{
    background: white;
    padding: 35px;
    border-radius: 15px;
    max-width: 600px;
    margin: 10px auto 0 auto;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}}
.cta-box h2 {{
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    color: black;
}}
.cta-box p {{
    text-align: center;
    margin-top: 12px;
    font-size: 18px;
    color: #444;
}}
.cta-buttons {{
    display: flex;
    justify-content: center;
    margin-top: 25px;
}}
.cta-buttons a {{
    text-decoration: none;
    font-weight: bold;
    padding: 14px 30px;
    border-radius: 30px;
    margin: 0 10px;
}}
.start-btn {{
    background: linear-gradient(90deg, #04AA6D, #2e77d0); /* Green-blue gradient */
    color: white !important; /* White text */
}}
.start-btn:hover {{
    opacity: 0.9;
    color: white !important; /* keep text white on hover */
}}
</style>
""", unsafe_allow_html=True)

# --- Navbar ---
st.markdown(f"""
<div class="navbar">
    <div class="navbar-left">
        <img src="data:image/png;base64,{logo_base64}">
    </div>
    <div class="navbar-center">
        <a href="#">Home</a>
        <a href="#">About</a>
        <a href="#">Contact</a>
    </div>
    <div class="navbar-right">
        <a href="#" class="login-btn">Login</a>
        <a href="#" class="signup-btn">Sign Up</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero">
    <h1>AI Health Monitoring System</h1>
    <p>Detects your mood and provides personalized recommendations for betterment</p>
    <div class="emoji-box">😊 😔 😴 😲 🤔</div>
</div>
""", unsafe_allow_html=True)

# --- Call To Action Section ---
st.markdown("""
<div class="cta-box">
    <h2>Get Started Today</h2>
    <p>Begin your journey to better mental health with our AI-powered mood detection and personalized wellness recommendations.</p>
    <div class="cta-buttons">
        <a href="#" class="start-btn">Start Mood Analysis</a>
    </div>
</div>
""", unsafe_allow_html=True)
