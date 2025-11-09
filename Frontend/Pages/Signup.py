import streamlit as st
from sidebar import load_sidebar 

LOGIN_PAGE = "Pages/Login.py"
DASHBOARD_PAGE = "Pages/Dashboard.py"

# Define navigation targets
LOGIN_PAGE = "Pages/Login.py"
DASHBOARD_PAGE = "Pages/Dashboard.py"

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Signup - HealthIQ", layout="wide", initial_sidebar_state="collapsed")

# 2. LOAD SIDEBAR
# This ensures the custom sidebar is loaded and the duplicate native one is hidden via CSS.
load_sidebar()

# 3. COMPLEX CSS INJECTION (Keeping your styles and fixing the sidebar issue)
st.markdown("""
<style>
    /* 🚨 FINAL FIX: HIDES THE AUTOMATIC PAGE LIST IN THE SIDEBAR */
    div[data-testid="stSidebarNav"] {
        display: none !important; 
    }
    
    /* --- Hides the 'Connecting' / Main Menu --- */
    #MainMenu, header {
        visibility: hidden;
    }
    
    /* 1. Basic reset and full-screen layout */
    .stApp {
        background-color: white;
        padding: 0;
        margin: 0;
        box-sizing: border-box;
    }
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }

    /* 2. Purple triangular section (right side) */
    .welcome-container {
        position: fixed;
        top: 0;
        right: 0;
        width: 100%; 
        height: 100vh;
        background: linear-gradient(135deg, #7F00FF, #000428);
        clip-path: polygon(40% 0%, 100% 0%, 100% 100%);
        z-index: 0;
    }

    .welcome-content {
        position: absolute;
        top: 40%;
        right: 5%; 
        transform: translateY(-50%);
        color: white;
        text-align: right; 
        width: 35%; 
        z-index: 2;
    }
    
    /* 3. Button styling */
    div.stButton button {
        background-color: #7A3F9D; /* Purple for action */
        color: white;
        font-weight: bold;
        padding: 10px 30px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }

    div.stButton button:hover {
        background-color: #5C2A7B; /* Darker purple on hover */
    }

    /* 4. Input field styling: white background, black text */
    div[data-testid="stTextInput"] input {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 10px;
        color: black !important;
        background-color: white !important;
        z-index: 10;
    }

    /* 5. Make labels and link visible on white background */
    label, .stMarkdown, .stCheckbox {
        color: black !important;
        z-index: 10;
        position: relative;
    }
    
    /* Link styling for Login */
    .login-link-container a {
        color: #7A3F9D !important;
        font-weight: bold;
        text-decoration: none;
        transition: color 0.2s;
    }
    .login-link-container a:hover {
        color: #5C2A7B !important;
    }
    
    /* Form alignment (Crucial for centered look) */
    .stContainer > div:nth-child(1) {
        max-width: 450px; /* Constrain form width */
        padding-left: 40px; /* Push content slightly right */
        padding-top: 60px; /* Push content down */
    }
            
    .login-spacer {
            /* Adjust height to control how high or low the form is */
            height: 10vh; /* Original was ~25vh. Reduce this to move up. */
    }
</style>
""", unsafe_allow_html=True)

# 4. BACKGROUND TRIANGLE (Right side)
st.markdown("""
    <div class="welcome-container">
        <div class="welcome-content">
            <h1 style='color: white; font-size: 4.5em; margin-bottom: 0.2em;'>Welcome to<br>HealthIQ.</h1>
            <p style='font-size: 0.8em;'>Join us and take control of your mental wellness journey today.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. SIGNUP FORM (Left side)
# We now use a smaller column ratio to push the form towards the center of the available white space.
col_padding, col_signup, col_placeholder = st.columns([0.3, 1.1, 1.5])

with col_signup:
    # Use padding to push the form down vertically
    st.markdown('<div class="login-spacer"></div>', unsafe_allow_html=True)
    
    # Message Placeholder (for errors/success)
    message_placeholder = st.empty()
    
    st.markdown("<h1 style='font-size: 2.5em; text-align: left; color: black !important;'>Create Account</h1>", unsafe_allow_html=True)
    
    # --- Input Fields ---
    username = st.text_input("Username", key="username_input", placeholder="Choose a username")
    email = st.text_input("Email", key="email_input", placeholder="Enter your email address")
    password = st.text_input("Password", type="password", key="password_input", placeholder="Create a password (min 6 chars)")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password_input", placeholder="Re-enter password")

    st.write("")
    
    # --- Action Buttons ---
    col_btn, col_link = st.columns([1, 1.2])
    
    with col_btn:
        signup_pressed = st.button("SIGNUP", key="signup_button", use_container_width=True)

        st.markdown("<p style='margin-top: 5px; color: black; text-align: center; font-weight:700; font-size: 1.4em;'>Already have an account?</p>", unsafe_allow_html=True)
        # Use the reliable Python button for navigation
        if st.button("Login", key="go_login_button_native", use_container_width=True):
            st.switch_page(LOGIN_PAGE)

# 6. SIGNUP LOGIC (Simulated Firebase Auth)
if st.session_state.get('signup_button'):
    # Get values, handling potential NoneType
    username = st.session_state.get('username_input', '').strip()
    email = st.session_state.get('email_input', '').strip()
    password = st.session_state.get('password_input', '')
    confirm_password = st.session_state.get('confirm_password_input', '')

    if not username or not email or not password or not confirm_password:
        message_placeholder.error("⚠ Please fill all fields.")
    elif password != confirm_password:
        message_placeholder.error("❌ Passwords do not match.")
    elif len(password) < 6:
        message_placeholder.error("❌ Password must be at least 6 characters long.")
    else:
        # Simulate successful Firebase Auth sign-up
        st.session_state['user_id'] = f'user_id_{username}'
        message_placeholder.success(f"✅ Signup successful! Welcome, {username}. Redirecting to Dashboard...")
        
        # Redirect to Dashboard immediately after successful signup
        st.switch_page(DASHBOARD_PAGE)