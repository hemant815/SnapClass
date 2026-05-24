import streamlit as st
import segno
import io
from src.database.config import supabase
import time
from src.database.db import enroll_student_to_subject


@st.dialog('Enroll in subject')
def enroll_dailog():
    st.write("Enter your subject code provided by your teacher to enroll")
    join_code=st.text_input('enter subject code ',placeholder='Eg. CSE101')

    if st.button('Enroll Now',type='primary',width='stretch'):
        if join_code:
            # response = supabase.table('subjects').select('subject , name, subject_code').eq('subject_code',join_code).execute()
            response = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code',join_code).execute()
            if response.data:
                subject = response.data[0]

                student_id = st.session_state.student_data['student_id']

                check = supabase.table('subject_students').select("*").eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()

                if check.data:
                    st.warning('you already Enrolled')

                else:
                    enroll_student_to_subject(student_id,subject['subject_id'])
                    st.success('successfull enrolled')
                    time.sleep(1)
                    st.rerun()



            else:
                st.warning('Please Enter valid code')
   