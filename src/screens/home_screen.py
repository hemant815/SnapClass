import streamlit as st
from src.components.header_home import header_home
from src.ui.base_layout import background_dashboard
from src.ui.base_layout import base_layout, background_home
from src.components.footer_home import footer_home



def home_screen():
    header_home()
    background_dashboard()
    base_layout()
    background_home()
    col1, col2 = st.columns(2,gap='large')

    
    
    with col1:
        st.markdown(
            "<h2 style='color:black;'>I'm Teacher</h2>",
            unsafe_allow_html=True
        )
        # st.image('./img/p2.png',width=120)
        st.image('./img/p.png',width=134)
        if st.button('Teacher Portal',type='primary',icon=":material/keyboard_double_arrow_right:",icon_position="right"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
        
    with col2:
        st.markdown(
            "<h2 style='color:black;'>I'm Student</h2>",
            unsafe_allow_html=True
        )
        st.image('./img/st.png',width=120)
        if st.button('Student Portal',type='primary',icon=":material/keyboard_double_arrow_right:",icon_position="right"):
            st.session_state['login_type'] = 'student'
            st.rerun()
    footer_home()

