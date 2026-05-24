import streamlit as st
import segno
from PIL import Image
from src.database.config import supabase
import time
from src.database.db import enroll_student_to_subject


@st.dialog('Add photo')
def add_photo_dailog():
    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []
    st.write("Add classroom photo to scan attendance")
    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        typecamera = 'primary' if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Camera',type=typecamera,width='stretch'):
            st.session_state.photo_tab='camera'
    with t2:
        typeupload = 'primary' if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('upload',type=typeupload,width='stretch'):
            st.session_state.photo_tab='upload'
    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take snap',key='dailog_cam')
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast('photo captured')
            st.rerun()
    if st.session_state.photo_tab == 'upload':
        upload_file = st.file_uploader('Choose photos',type=['jpg','png','jpeg'],accept_multiple_files=True,key='dailog_upload')
        if upload_file:
            for f in upload_file:
                st.session_state.attendance_images.append(Image.open(f))
                st.toast('Photos upload Successfully')
                st.rerun()
    st.divider()
    
    if st.button('Done',type='primary',width='stretch'):
        st.rerun()
