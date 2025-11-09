import streamlit as st
import base64
import os
from sidebar import load_sidebar 
import re

st.set_page_config(page_title="Contact Us", layout="wide")

# 2. LOAD SIDEBAR (Creates the custom navigation you want to keep)
try:
    load_sidebar()
except Exception:
    # If sidebar cannot be loaded, continue without it to avoid breaking the app.
    st.warning("Sidebar could not be loaded.")

def get_base64(file):
    """Encodes the image file to base64."""
    if not os.path.exists(file):
        st.error(f"❌ Background Image not found at: {file}")
        return ""
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background_and_styles(image_path):
    """Set the background image and custom CSS for aesthetics."""
    
    encoded = get_base64(image_path)
    if not encoded:
        return # Stop if image loading failed

    # 2. Custom CSS for Styling
    st.markdown(f"""
        <style>
        /* 🚨 FIX: HIDES THE AUTOMATIC PAGE LIST IN THE SIDEBAR */
        div[data-testid="stSidebarNav"] {{
            display: none !important; 
        }}
        /* --- Optional: Hides the 'Connecting' / Main Menu --- */
        #MainMenu, header {{
            visibility: hidden;
        }}
        
        /* --- Background Container --- */
        [data-testid="stAppViewContainer"] {{
            background: url("data:image/jpg;base64,{encoded}") no-repeat center center fixed;
            background-size: cover;
            font-family: 'Arial', sans-serif;
        }}

        /* --- Main Content Box (Pushes form to Top-Right) --- */
        .contact-box {{
            /* Removes the internal image overlay which was causing alignment issues */
            background-color: rgba(255, 255, 255, 0.92); 
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
            max-width: 650px; 
            
            /* --- FIX: PUSH TO TOP AND ALIGN RIGHT --- */
            margin: 30vh 0 0 auto; 
            margin-right: 0 !important; /* Ensures it sticks to the far right of its column */
        }}
        
        /* --- Form Centering in the container --- */
        div[data-testid="stVerticalBlock"] {{
            max-width: 400px;
            margin: 0 0 0 auto; 
            margin-right: 0 !important;
        }}

        /* --- Title and Headers --- */
        h1 {{
            color: #000066 !important;
            text-align: center; 
            margin-bottom: 30px;
            font-size: 2.5em;
        }}

        /* --- Button Style (Styles retained) --- */
        div.stButton > button:first-child {{
            background-color: #000066 !important;
            color: #ffffff !important;
            font-weight: bold !important;
            border-radius: 12px !important;
            padding: 12px 35px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 102, 0.3);
            display: block; 
            margin: 20px auto 0 auto; 
        }}
        </style>
    """, unsafe_allow_html=True)


# --- Page Content Function ---
def show_contact_content():
    """Renders the main content of the contact page."""
    
    # Apply the background and custom CSS
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "Contactbg.jpg")
    
    set_background_and_styles(image_path)
    
    # Use 3 columns to push the main content box into the center-right area
    col_padding_left, col_main_content, col_padding_right = st.columns([0.5, 50, 0.5]) # Adjusted ratio for right push

    with col_main_content: 

        st.markdown("### 📧 Send Us a Message")

        # --- Form ---
        with st.form(key='contact_form', clear_on_submit=True):
            name = st.text_input("Your Name", placeholder="Enter your name")
            email = st.text_input("Your Email", placeholder="Enter your email")
            message = st.text_area("Your Message", placeholder="Type your detailed message here...", height=150)

            if st.form_submit_button("Send Message"):
                # --- NEW VALIDATION LOGIC ---
                
                # 1. Check for empty fields
                if not name or not email or not message:
                    st.warning("⚠️ Please fill all fields.")
                
                # 2. Name Validation (No numbers/digits allowed)
                elif re.search(r'\d', name):
                    st.error("❌ Name cannot contain numbers.")
                
                # 3. Email Validation (Must contain @ and a dot .)
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error("❌ Please enter a valid email address.")
                    
                if not name or not email or not message:
                    st.warning("⚠️ Please fill all fields.")
                else:
                    st.success(f"✅ Thank you, {name}! Your message has been sent successfully. We will follow up at {email}.")

        st.markdown('</div>', unsafe_allow_html=True)


# --- Render the Contact Page Content ---
if __name__ == '__main__':
    show_contact_content()