import streamlit as st
from src.database.db import create_subject


@st.dialog('Create new Subject')
def create_subject_dailog(teacher_id):
    st.write('Enter the details of new subject')
    sub_id = st.text_input('Subject code',placeholder='CS102')
    sub_name = st.text_input('Subject name',placeholder='computer science')
    sub_section = st.text_input('Subject section',placeholder='A')

    if st.button('Create Subject Now',type='primary',width='stretch'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(
                    sub_id,
                    sub_name,
                    sub_section,
                    teacher_id
                )
                st.rerun()
            except Exception as e:
                st.error(f"error: {str(e)}")
        else:
            st.warning('fill complate details')