import streamlit as st
import base64

with open("path_to_image.png", "rb") as image_file:
    img_base64 = base64.b64encode(image_file.read()).decode("utf-8")

st.markdown(f"""
    <div style="text-align: right;">
        <img src="data:image/png;base64,{img_base64}" width="400"/>
    </div>
    """, unsafe_allow_html=True)
