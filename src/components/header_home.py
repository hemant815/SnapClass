import streamlit as st


def header_home():
    url_img = 'https://i.ibb.co/YTYGn5qV/logo.png'
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:10px;">
            <img src = '{url_img}' style='height:100px;'/> 
            <h1 style='text-align:center; color:#E0E3FF;'>SNAP<br/>CLASS</h1>
        </div>
        """,unsafe_allow_html=True)
