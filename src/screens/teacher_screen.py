import streamlit as st
from src.ui.base_layout  import background_dashboard , base_layout
from src.components.header_home import header_dashboard
from src.components.footer_home import footer_dashboard,footer_home
from src.database.db import check_teacher_exist, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher
import time
from src.components.dailog_create_subject import create_subject_dailog
from src.components.subject_card import subject_card
from src.components.dailog_share_subject import share_subject_dialog
from src.components.dailog_add_photo import add_photo_dailog
from src.pipelines.face_pipeline import predict_attendance
import numpy as np
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.dailog_attendance_result import attendance_result_dailog
from src.components.dialog_voice_attendance import dialog_voice_attendance

def teacher_screen():
    background_dashboard()
    base_layout()
    
    if "teacher_data" in st. session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state. teacher_login_type==" login":
        teacher_screen_login()
    elif st. session_state. teacher_login_type == "register":
        teacher_register_screen()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    col1,col2 = st.columns(2, vertical_alignment='center',gap='xlarge')
    with col1:
        header_dashboard()
    with col2:
        st.subheader(f"welcome {teacher_data['name']}")
        if st.button('Logout',type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['is_login_in']= False
            del st.session_state.teacher_data
            st.rerun()
    st.space()
    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab ='take_attendance'
    tab1,tab2,tab3 = st.columns(3)

    with tab1:
        type1='primary' if st.session_state.current_teacher_tab == 'take_attendance' else 'tertiary'
        if st.button('Take Attendance',width='stretch',type=type1,icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()
    with tab2:
        type2 = 'primary' if st.session_state.current_teacher_tab == 'manage_subject' else 'tertiary'
        if st.button('Manage Subject',width='stretch',type=type2,icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subject'
            st.rerun()
    with tab3:
        type3= 'primary' if st.session_state.current_teacher_tab == 'attendance_records' else 'tertiary'
        if st.button('Attendance Records',width='stretch',type=type3,icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    if st.session_state.current_teacher_tab == 'take_attendance':
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == 'manage_subject':
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == 'attendance_records':
        teacher_tab_attendance_records()
    footer_home()
def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']

    st.header('Attendance')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images=[]
    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('you havent created please create first')
        return
    subject_option = {f"{s['name']} - {s['subject_code']} ":s['subject_id'] for s in subjects}
    
    col1, col2 = st.columns([3,1],vertical_alignment='bottom')

    with col1:
        selected_subject = st.selectbox('Select subject',options=list(subject_option.keys()))

    with col2:

        if st.button('➕ Add Photos',type='primary'):
            add_photo_dailog()

    selected_subject_id = subject_option[selected_subject]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added images')
        gallery_col = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_col[idx%4]:
                st.image(img,width='stretch',caption=f"photo {idx+1}")
    photos = bool(st.session_state.attendance_images)
    c1,c2,c3 = st.columns(3)
    with c1:
        photos = bool(st.session_state.attendance_images)
        if st.button("Clear All Photo",width='stretch',type='tertiary',icon=':material/delete:',disabled=not photos):
            st.session_state.attendance_images = []
            st.rerun()
    with c2:
        
        if st.button("Run Face Analysis",width='stretch',type='secondary',icon=':material/analytics:',disabled=not photos):
            with st.spinner('Deep scanning classroom photos'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))

                    detected,_ ,_ = predict_attendance(img_np)
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id,[]).append(f"photo{idx+1}")
                enrolled_res = supabase.table('subject_students').select('*, students(*)').eq('subject_id',selected_subject_id).execute()
                enrolled_student = enrolled_res.data

                if not enrolled_student:
                    st.warning('No Enrolled Student in this subject')
                else:
                    result,attendance_logs= [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_student:
                        student=node['students']
                        source = all_detected_ids.get(int(student['student_id']),[])
                        is_present = len(source) > 0

                        result.append({
                            "Name": student['name'],
                            "ID":student['student_id'],
                            "source":", ".join(source) if is_present else "_",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_logs.append({
                            'student_id':student['student_id'],
                            'subject_id':selected_subject_id,
                            'timestamp':current_timestamp,
                            'is_present':bool(is_present)

                        })
                    attendance_result_dailog(pd.DataFrame(result),attendance_logs)


    with c3:
        if st.button("Voice attendance",width='stretch',type='primary',icon=':material/mic:'):
            dialog_voice_attendance(selected_subject_id)

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<h2 style='color:black; padding:0;'>Manage Subjects</h2>",
            unsafe_allow_html=True
        )

    with col2:
        if st.button('Create New Subject',width='stretch'):
            create_subject_dailog(teacher_id)
    subjects=get_teacher_subjects(teacher_id)
    if subjects: 
        for sub in subjects:
            stats=[('👨🏻‍🎓',"Students", sub['total_students']),
                    ("🕣","Classes",sub ['total_classes'])
                ]
            def share_btn() :
                if st. button(f"Share Code: {sub ['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(sub["name"], sub["subject_code"])
            st.space()
            subject_card(
            name = sub['name'],
            code = sub["subject_code"],
            section =sub['section'],
            stats=stats,
            footer_callback=share_btn)
    else:
        st. info("NO SUBJECTS FOUND, CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    st.header('Atteadance Records')
    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)
    if not records:
        return
    data = []

    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group":ts.split(".")[0] if ts else None,
            "Time":datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            "Subject":r['subjects']['name'],
            "subject_code":r['subjects']['subject_code'],
            "is_present":bool(r.get('is_present',False))
        })

    df = pd.DataFrame(data)

    summary=(
        df.groupby(['ts_group',"Time",'Subject',"subject_code","is_present"]).agg(
            Present_count=("is_present",'sum'),
            Total_count=("is_present",'count')
        ).reset_index()
    )
    summary['Attendance Stats'] = (
        "✅" + summary['Present_count'].astype(str) + "/"
          + summary['Total_count'].astype(str)

    )
    display_df = (summary.sort_values(by='ts_group',ascending=False)
                  [['Time','Subject','subject_code','Attendance Stats']])
    st.dataframe(display_df,width='stretch',hide_index=True)


    records = get_attendance_for_teacher(teacher_id)
def login_teacher (username, password):
        if not username or not password:
            return False
        teacher = teacher_login(username, password)
        if teacher:
            st.session_state. user_role ='teacher' 
            st. session_state. teacher_data= teacher
            st.session_state.is_logged_in = True
            return True
        return False
def teacher_screen_login():
    col1,col2 = st.columns(2, vertical_alignment='center',gap='xlarge')
    with col1:
        header_dashboard()
        

    with col2:
        if st.button('Go back to Home',type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['login_type']=None
            st.rerun()
    st.markdown(
            "<h2 style='color:black; text-align: center;'>Login using Password</h2>",
            unsafe_allow_html=True
        )
    st.space()
    st.space()
    teacher_user = st.text_input('Enter username',placeholder='@ananyaroy')
    teacher_password = st.text_input("Enter password",type='password',placeholder='Enter password')
    st.divider()
    btn1,btn2 = st.columns(2)

    with btn1:
        if st.button('Login',icon=":material/passkey:",shortcut='command+enter',width='stretch'):
            if login_teacher(teacher_user,teacher_password):
            # if teacher_login(teacher_user,teacher_password):
                st.toast('Welcome back! ',icon="👋🏻")
                time.sleep(1)
                st.rerun()
            else:
                st.error('Invailed username or password')

    with btn2:
        if st.button('Register Instead',icon=":material/passkey:",width='stretch',type='primary'):
            st.session_state.teacher_login_type ='register'
    footer_dashboard()
def register_teacher(teacher_username, teacher_name,teacher_password, confirm_password):
    if not teacher_username or not teacher_name or not teacher_password:
        return False, 'All Field Required'
    if check_teacher_exist(teacher_username):
        return False, 'User Exist'
    if teacher_password != confirm_password:
        return False, 'Password dont match'
    try:
        create_teacher(teacher_username,teacher_password,teacher_name)
        return True , 'Successful Created! login Now '
    except Exception as e:
        return False, str(e)


def teacher_register_screen():
    col1,col2 = st.columns(2, vertical_alignment='center',gap='xlarge')
    with col1:
        header_dashboard()
        

    with col2:
        if st.button('Go back to Home',type='secondary',key='loginbackbtn',shortcut='control+backspace'):
            st.session_state['login_type']=None
            st.rerun()
    st.markdown(
            "<h2 style='color:black;'>Register your teacher profile</h2>",
            unsafe_allow_html=True
    )
    st.space()
    teacher_username = st.text_input('Enter username',placeholder='@ananyaroy')
    teacher_name = st.text_input('Enter name',placeholder='ananya')
    teacher_password = st.text_input("Enter password",type='password',placeholder='Enter password')
    confirm_password = st.text_input("confirm password",type='password',placeholder='Re-enter password')
    st.divider()
    btn1,btn2 = st.columns(2)

    with btn1:
        if st.button('Register',icon=":material/passkey:",shortcut='command+enter',width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name,teacher_password, confirm_password)
            if success:
                st.success('message')
                time.sleep(2)
                st.session_state.teacher_login_type ='login'
                st.rerun()
            else:
                st.error(message)



    with btn2:
        if st.button('Login Instead',icon=":material/passkey:",width='stretch',type='primary'):
            st.session_state.teacher_login_type ='login'
    footer_dashboard()