import streamlit as st
from sidebar import load_sidebar 

# Define navigation targets
DASHBOARD_PAGE = "Pages/Dashboard.py"
SIGNUP_PAGE = "Pages/Signup.py"

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Login - HealthIQ", layout="wide", initial_sidebar_state="collapsed")

# 2. LOAD SIDEBAR
load_sidebar() 

# 3. COMPLEX CSS INJECTION (Kept for continuity and duplicate sidebar fix)
st.markdown(
    """
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

    .welcome-content h1 {
        font-size: 4.5em; 
        margin-bottom: 0.2em;
        text-align: right;
        color: white;
    }

    /* 3. Login Button styling - Primary Login Button */
    div.stButton button[key="login_button"] {
        background-color: #7A3F9D; 
        color: white;
        font-weight: bold;
        padding: 10px 30px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }
    div.stButton button[key="login_button"]:hover {
        background-color: #5C2A7B;
    }

    /* Create Account Button (Secondary style, same as Signup) */
    div.stButton button[key="go_signup_button"] {
        background-color: #5C2A7B; /* Slightly darker to differentiate from LOGIN */
        color: white;
        font-weight: bold;
        padding: 10px 30px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    div.stButton button[key="go_signup_button"]:hover {
        background-color: #4A1E5C;
    }
    div.stContainer {
        border: 1px solid #ddd; /* Light grey border */
        border-radius: 8px;
        padding: 20px !important; 
        background-color: #fcfcfc; /* Off-white background to stand out */
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        max-width: 450px; /* Constrain its size */
    }


    /* 4. Input field styling */
    div[data-testid="stTextInput"] input {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 10px;
        color: black !important;
        background-color: white !important;
        z-index: 10;
    }

    /* 5. Labels and Links */
    label, .stMarkdown, .stCheckbox {
        color: black !important;
        z-index: 10;
        position: relative;
    }

    /* Link styling for Signup */
    .signup-link-text a {
        color: #7A3F9D !important;
        font-weight: bold;
        text-decoration: none;
        transition: color 0.2s;
    }
    .signup-link-text a:hover {
        color: #5C2A7B !important;
    }
    /* ADD THIS TO YOUR <style> BLOCK */
    .login-spacer {
    /* Adjust height to control how high or low the form is */
        height: 22vh; /* Original was ~25vh. Reduce this to move up. */
    }

    div[data-testid="stException"] {
        background-color: black !important; /* Pure Black Background */
        color: white !important; /* White text for high visibility */
        border: 2px solid #FF5555; /* Red border for emphasis */
        border-radius: 8px;
        padding: 15px;
    }
    div[data-testid="stAlert"] [data-baseweb="alert"] {
        background-color: #330000 !important; /* Dark Red Background for st.error */
        color: #FFDDDD !important; /* Light red text */
}

    </style>
    """,
    unsafe_allow_html=True
)

# 4. BACKGROUND TRIANGLE (Right side)
st.markdown("""
    <div class="welcome-container">
        <div class="welcome-content">
            <h1 style='color: white; font-size: 4.5em; margin-bottom: 0.2em;'>Welcome to<br>HealthIQ.</h1>
            <p style='font-size: 0.8em;'>Join us and take control of your mental wellness journey today.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. LOGIN FORM (Left side)
# New column setup to center the form within the white space
col_padding_left, col_login, col_placeholder = st.columns([0.4, 1.1, 1.5]) 

with col_login:

    st.markdown('<div class="login-spacer"></div>', unsafe_allow_html=True)
    # Form Title
    st.markdown("<h1 style='font-size: 2.9em; text-align: left; color: black !important;'>Login</h1>", unsafe_allow_html=True)
    
    # Initialize message placeholder
    message_placeholder = st.empty()
    
    # --- Input Fields ---
    username = st.text_input("Email / Username", key="username_input", placeholder="Enter your email or username")
    password = st.text_input("Password", type="password", key="password_input", placeholder="Enter your password")
    
    st.write("")
    
    # --- Action Buttons Container ---
    col_btn_login, col_btn_signup = st.columns([1, 1])
    
    with col_btn_login:
         # Primary Login Button (takes 1/2 the width)
        login_pressed = st.button("LOGIN", key="login_button", use_container_width=True)

    with col_btn_signup:
        # Create Account Button (takes 1/2 the width)
        if st.button("Create Account", key="go_signup_button", use_container_width=True):
             st.switch_page(SIGNUP_PAGE)

    # Small Sign-up link below the buttons
    st.markdown(
        f"<div style='margin-top: 15px; text-align: center;' class='signup-link-text'>Don't have an account? <a href='javascript:void(0)' onclick='window.parent.location.href = \"?page=Signup.py\"'>Signup</a></div>", 
        unsafe_allow_html=True
    )


# 6. LOGIN LOGIC (Simulated Firebase Auth)
if st.session_state.get('login_button'):
    # In a real app, you would call Firebase Auth here
    
    if username and password:
        # Simulate successful Firebase Auth sign-in
        if username == "test@healthiq.com" and password == "123456":
            
            # --- Successful Login ---
            st.session_state['user_id'] = 'unique_user_id_from_firebase'
            message_placeholder.success(f"✅ Login successful! Redirecting to dashboard...")
            st.toast("Welcome back!", icon="👋")
            
            # Use st.switch_page for redirection after successful login
            st.switch_page(DASHBOARD_PAGE)
            
        else:
            message_placeholder.error("❌ Invalid username or password. Please try again.")
    else:
        message_placeholder.warning("⚠️ Please enter both email and password.")