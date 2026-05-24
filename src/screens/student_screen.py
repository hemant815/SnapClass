import streamlit as st
from src.ui.base_layout  import background_dashboard , base_layout
from src.components.header_home import header_dashboard
from src.components.footer_home import footer_dashboard,footer_home
from src.database.db import get_enrolled_subject, get_student_attendance #,check_teacher_exist, create_teacher, teacher_login ,
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance,get_face_embedding,trained_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, enroll_student_to_subject, unenroll_student_to_subject
import time
from src.components.enroll_dailog import enroll_dailog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    
    col1,col2 = st.columns(2, vertical_alignment='center',gap='xlarge')
    with col1:
        header_dashboard()
    with col2:
        st.subheader(f"welcome {student_data['name']}")
        if st.button('Logout',type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['is_login_in']= False
            del st.session_state.student_data
            st.rerun()
    st.space()
    c1,c2 = st.columns(2)
    with c1:
        st.header('Your Enrolled Subject')

    with c2:
        if st.button('Enroll in Subject',type='primary',width='stretch'):
            enroll_dailog()

    st.divider()
    with st.spinner('Your enrolled subject Loading'):
        subject = get_enrolled_subject(student_id)
        logs = get_student_attendance(student_id)
    # st.write(logs)
    # st.write(subject)
    stats_map = {}
    for log in logs:
        sid= log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total":0,"attended": 0}
        stats_map[sid]['total'] +=1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1
    cols = st.columns (2)
    for i, sub_node in enumerate(subject):
            sub = sub_node['subjects']
            sid = sub['subject_id']

            stats=stats_map.get(sid,{'total':0,"attended":0})
            def unenroll_btn():
                if st.button('Unenroll from this course',type='tertiary',width='stretch',key=f'unenroll_{sid}'):
                    unenroll_student_to_subject(student_id,sid)
                    st.toast(f"Successfully Unenrolled subject{sub['name']}")
                    st.rerun()


            with cols [i % 2]:
                subject_card(
                    name = sub['name'],
                    code = sub['subject_code'],
                    section = sub['section'],
                    stats=[
                        ("🗓️",'Total',stats['total']),
                        ("✅",'attended',stats['attended'])
                    ]
                    ,footer_callback=unenroll_btn

                )



        
    footer_home()
    

def student_screen():
    background_dashboard()
    base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return 
    
    col1,col2 = st.columns(2, vertical_alignment='center',gap='xlarge')
    with col1:
        header_dashboard()
    

    with col2:
        if st.button('Go back to Home',type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['login_type']=None
            st.rerun()
    st.markdown(
            "<h2 style='color:black; text-align: center;'>Login using FaceID</h2>",
            unsafe_allow_html=True
        
        )
    show_registration = False
    img_source= st.camera_input('Position your face in the center')
    if img_source:
        img = np.array(Image.open(img_source))
        with st.spinner('AI is Scanning..'):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('face not found')
            elif num_faces >= 2:
                st.warning('multiple faces')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_student = get_all_students()
                    student = next((s for s in all_student if s['student_id']==student_id),None)

                    if student:
                        st.session_state.is_logged_in =True
                        st.session_state.user_role ='student'
                        st.session_state.student_data = student
                        st.toast(f'Welcome Back {student['name']}')
                        time.sleep(1)
                        st.rerun()

                else:
                    st.error('face not recognited you might new student')
                    show_registration =True

    if show_registration:
        with st.container(border =True):
            st.header('Register now profile')
            new_name = st.text_input('enter your name',placeholder='E.g. rahul')
            st.subheader('optional : voice Enrollment')
            st.info('Enroll your voice only attandance')


            audio_data = None
            try:
                audio_data = st.audio_input('record your phrase like i am present')
            except Exception:
                st.error('audio data failed')
            if st.button('Create Account',type='primary'):
                if new_name:
                    with st.spinner('Creating Profile...'):
                        img = np.array(Image.open(img_source))
                        embedding = get_face_embedding(img)
                        if embedding:
                            face_emb = embedding[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_emb,voice_emb)
                            if response_data:
                                trained_classifier()
                                st.session_state.is_logged_in =True
                                st.session_state.user_role ='student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'Profile Created! HI {new_name}')
                                time.sleep(1)
                                st.rerun()

                        else:
                            st.error('face not capture')





                else:
                    st.warning('please enter your name')

    footer_dashboard()