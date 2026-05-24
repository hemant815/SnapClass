import streamlit as st


def footer_home():
    url_img = "https://i.ibb.co/4r5X1FY/apnacollege.png"
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-algin:center; ">
                <p style="color:black">Created with ❤️ by </p>
                <img src='{url_img}' style="max-height:25px;"/>
        </div>
        """,unsafe_allow_html=True)
def footer_dashboard():
    url_img = "https://i.ibb.co/4r5X1FY/apnacollege.png"
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-algin:center; ">
                <p style="color:white">Created with ❤️ by </p>
                <img src='{url_img}' style="max-height:25px;"/>
        </div>
        """,unsafe_allow_html=True)
