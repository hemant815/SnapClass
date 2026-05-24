import streamlit as st
from src.database.db import create_attendance
import time


def show_attendance_result(df,logs):
    st.write('Please review attendance before submit')
    st.dataframe(df,hide_index=True,width='stretch')

    c1,c2 = st.columns(2)

    with c1:
        if st.button('Discard',width='stretch',type='secondary'):
            st.session_state.voice_attendance_result=None
            st.session_state.attendance_images=[]
            st.rerun()

    with c2:
        if st.button('Confirm & Save',width='stretch',type='primary'):
            try:
                create_attendance(logs)
                st.success("Attendance Taken")
                st.session_state.attendance_images=[]
                st.session_state.voice_attendance_result=None
                time.sleep(1)
                st.rerun()

            except Exception as e:
                st.error("Sync Failed")
@st.dialog('Attendance Reports')
def attendance_result_dailog(df,logs):
    show_attendance_result(df,logs)