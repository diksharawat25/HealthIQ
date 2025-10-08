import streamlit as st
import base64
import os

st.set_page_config(page_title="About the System", layout="wide")

# ---------- Background image ----------
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Base directory of this script
BASE_DIR = os.path.dirname(__file__)

# Background image path (inside Frontend/about/)
bg_path = os.path.join(BASE_DIR, "aboutbg.jpeg")
bg_img = get_base64(bg_path)

# Inject CSS for background and gradient heading
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{bg_img}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
.gradient-heading {{
    text-align: center;
    font-size: 80px; /* Heading larger */
    font-weight: bold;
    background: linear-gradient(to right, #00ff99, #0099ff); /* green → blue */
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
</style>
""", unsafe_allow_html=True)

# ---------- Page Content ----------
st.markdown("<h1 class='gradient-heading'>About the System</h1>", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([1,1])

with col1:
    st.markdown("""
    <div style="background: rgba(255,255,255,0); padding:20px; border-radius:10px;">
        <p style="font-size:20px; line-height:1.8; text-align:justify; color:#000000;">
        The <b>AI Health Monitoring System</b> monitors mental well-being by detecting mood from text and facial expressions. 
        It tracks emotional trends, provides personalized guidance, and shows progress on a dashboard, ensuring data privacy 
        while offering real-time support for better mental health.
        </p>
        <h3 style="color:#00aa88; font-size:22px;">Features</h3>
        <ul style="font-size:18px; line-height:1.8; color:#000000;">
            <li><b>Mood Detection:</b> Analyze text and facial expressions.</li>
            <li><b>Emotional Trend Analysis:</b> Track patterns over time.</li>
            <li><b>Personalized Guidance:</b> Suggest exercises, journaling, and tips.</li>
            <li><b>Progress Dashboard:</b> Visualize improvements and milestones.</li>
            <li><b>Alerts & Security:</b> Keep data safe and anonymized.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Right-aligned PNG image without box or shadow
    image_path = os.path.join(BASE_DIR, "imageOfabout.png")
    img_base64 = get_base64(image_path)

    st.markdown(f"""
    <div style="text-align: right;">
        <img src="data:image/png;base64,{img_base64}" width="500"/>
    </div>
    """, unsafe_allow_html=True)

