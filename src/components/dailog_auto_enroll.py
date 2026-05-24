import streamlit as st
import segno
import io
from src.database.config import supabase
import time
from src.database.db import enroll_student_to_subject



@st.dialog('Auto join class')
def auto_enroll_dailog(subject_code):
    student_id = st.session_state.student_data['student_id']

    res = supabase.table('subjects').select("*").eq('subject_code',subject_code).execute()

    if not res.data:
        st.error('Subject Code not found!')
        if st.button('Close'):
            st.query_params.clear()
            st.rerun()
        return 
    
    subject = res.data[0]
    check = supabase.table('subject_students').select("*").eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()
    if check.data:
        st.info('Already Enrolled')
        if st.button('Got it'):
            st.query_params.clear()
            st.rerun()
        return
    st.markdown(f"Would you like to enroll in **{subject['name']}**?")
    c1,c2 = st.columns(2)
    with c1:
        if st.button('No Thanks!'):
            st.query_params.clear()
            # st.rerun()
    with c2:
        if st.button('Yes Enrolled Now',type='primary'):
                enroll_student_to_subject(student_id,subject['subject_id'])
                st.toast('successfully join')
                st.query_params.clear()
                time.sleep(2)
                st.rerun()




   