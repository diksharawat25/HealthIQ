import streamlit as st
import base64
import os
from sidebar import load_sidebar

st.set_page_config(page_title="About the System", layout="wide")

# Load Sidebar
load_sidebar()

# ---------- Background image ----------
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

BASE_DIR = os.path.dirname(__file__)
bg_path = os.path.join(BASE_DIR, "aboutbg.jpeg")
bg_img = get_base64(bg_path)

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
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{bg_img}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
.gradient-heading {{
    text-align: center;
    font-size: 80px;
    font-weight: bold;
    background: linear-gradient(to right, #32CD32, #00BFFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
</style>
""", unsafe_allow_html=True)

# ---------- Page Content ----------
st.markdown("<h1 class='gradient-heading' style='padding-bottom: 20px;'>About the System</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("""
    <div style="background: rgba(255,255,255,0); padding:20px; border-radius:10px;">
        <p style="font-size:18px; line-height:1.8; text-align:justify; color:#000000; ">
        The <b>AI Health Monitoring System</b> that focuses on detecting and understanding an individual’s mood to promote better mental health awareness. The main goal of this system is to help users monitor their emotional state and get insights that can support their overall well-being. When a user signs up, they are guided through a simple psychological assessment designed to evaluate their current mental state. Once completed, they gain access to a personalized dashboard where all their emotional data, assessment results, and progress are displayed in an easy-to-understand format. The system takes input from both text and voice, analyzing them through intelligent algorithms to detect patterns in mood and emotional tone. Based on these analyses, the platform provides meaningful insights that help users become more aware of their emotional health. All user information, mood scores, and activity logs are securely stored, ensuring privacy and data safety. With its interactive design and AI-driven capabilities, HealthIQ serves as a smart companion for users who want to stay connected with their mental and emotional wellness.        </p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    image_path = os.path.join(BASE_DIR, "imageOfabout.png")
    img_base64 = get_base64(image_path)
    st.markdown(f"""<div style="text-align:right; padding-bottom: 10vh;"><img src="data:image/png;base64,{img_base64}" width="600" style="padding-bottom: 10vh;"/></div>""", unsafe_allow_html=True)
