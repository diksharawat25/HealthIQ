import streamlit as st
import base64
import os

def load_sidebar():
    """Sidebar with logo at the top, white background, and navy blue text"""
    st.markdown("""
        <style>
        /* Sidebar white background + text color */
        [data-testid="stSidebar"] {
            background-color: white !important;
            color: #1f4e79 !important;
            border-right: 1px solid #ddd;
        }

        [data-testid="stSidebar"] * {
            color: #1f4e79 !important;
            font-weight: 600 !important;
        }

        /* Logo at the top */
        .sidebar-logo {
            display: block;
            margin: 20px auto 30px auto;
            width: 130px;
        }

        /* Adjust sidebar padding */
        section[data-testid="stSidebarNav"] {
            padding-top: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    BASE_DIR = os.path.dirname(__file__)
    logo_path = os.path.join(BASE_DIR, "logo.png")

    # ---- Logo display at top ----
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
        st.sidebar.markdown(
            f'<img src="data:image/png;base64,{logo_base64}" class="sidebar-logo" alt="Logo"/>',
            unsafe_allow_html=True
        )
    else:
        st.sidebar.markdown("### 🩺 HealthIQ")

    # ---- Navigation Links ----

    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("Pages/about.py", label="ℹ️ About")
    st.sidebar.page_link("Pages/contact.py", label="📞 Contact")
    st.sidebar.page_link("Pages/login.py", label="🔐 Login")
    st.sidebar.page_link("Pages/signup.py", label="📝 Signup")

    st.sidebar.markdown("---")
    st.sidebar.caption("© 2025 HealthIQ")
