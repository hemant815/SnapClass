import streamlit as st
def background_home():

    st.markdown("""
        <style>
                .stApp {
                    background: #4BB8FA !important;
                }
                .stApp div[data-testid='stColumn']{
                background-color:#C4E2F5 !important;
                border-radius: 4rem !important;
                padding:2.5rem !important;
                }
                
                
        </style>
            """,unsafe_allow_html=True
    )
def background_dashboard():

    st.markdown("""
        <style>
                .stApp {
                    background: #4BB8FA !important;
                }
                
                
        </style>
            """,unsafe_allow_html=True
    )
def base_layout():

    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
            #MainMenu, footer, header {
                visibility: hidden;
                }
            .block-container{
                padding-top:1.5rem !important;
                }
            h1, h2{
                font-family:"Climate crisis", sans-sarif !important;
                font-size:2.5 rem !important;
                line-height:1 !important;
                margin-bottom: 0 rem !important;
                

                }
            h3, h4, p{
                font-family: 'Outfit','sans-sarif'
                }
            button{
                background:#4BB8FA !important;
                border-radius:1.8 rem !important;
                color: white !important;
                border:none !important;
                padding: 10px 20px !important;
                transition:tranform 0.25s ease-in-out !important;
                }
            button[kind='secondary']{
                background:#EB459E !important;
                border-radius:1.8 rem !important;
                color: white !important;
                border:none !important;
                padding: 10px 20px !important;
                transition:tranform 0.25s ease-in-out !important;
                }
            button[kind='tertiary']{
                background: black !important;
                border-radius:1.8 rem !important;
                color: white !important;
                border:none !important;
                padding: 10px 20px !important;
                transition:transform 0.25s ease-in-out !important;
                }

            button:hover{
                transform: scale(1.05);
                }
        </style>
            """,unsafe_allow_html=True
    )