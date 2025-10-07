import streamlit as st

st.set_page_config(page_title="Contact Us", layout="wide")

# ---------- CSS for styling ----------
st.markdown("""
<style>
body {
    background-color: #0f0f0f;
    color: white;
    font-family: Arial, sans-serif;
}

.contact-box {
    background-color: rgba(0,0,0,0.0); /* Transparent */
    color: black;
    padding: 30px;
    border-radius: 10px;
}

input, textarea {
    color: black;
}

.stButton>button {
    background-color: white;
    color: black;
    font-weight: bold;
}

.alert {
    padding: 15px;
    border-radius: 5px;
    margin-top: 15px;
}

.alert-error {
    background-color: #f8d7da;
    color: #721c24;
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
}
</style>
""", unsafe_allow_html=True)

st.title("Contact Us")

# ---------- Layout ----------
left_col, right_col = st.columns(2)

with left_col:
    st.markdown('<div class="contact-box">', unsafe_allow_html=True)
    st.markdown("**Delhi Road, ABC Building**")
    st.markdown("Roorkee, Uttrakhand")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**+91 7037XXXXXX**")
    st.markdown("Monday to Saturday, 10 A.M to P.M")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**basudhachauhan685@gmail.com**")
    st.markdown("Email us your query")
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    name = st.text_input("Your Name", placeholder="Enter your name")
    email = st.text_input("Your Email", placeholder="Enter your Email")
    message = st.text_area("Your Message", placeholder="Enter Your message", height=150)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Send Message"):
        if not name or not email or not message:
            st.markdown('<div class="alert alert-error">⚠️ Please fill in all required fields marked with * before submitting.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert alert-success">✅ Your message has been sent successfully!</div>', unsafe_allow_html=True)
            # Optionally, here you can add code to send the email or save the message
