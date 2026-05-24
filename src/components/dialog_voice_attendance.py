import streamlit as st
from datetime import datetime
import pandas as pd
from src.database.config import supabase
from src.pipelines.voice_pipeline import process_bulk

from src.components.dailog_attendance_result import show_attendance_result

@st.dialog('Auto join class')
def dialog_voice_attendance(subject_code):
    st.write('Record students audio saying present then AI recognice the students')

    audio_data= None

    audio_data =st.audio_input('Record classroom audio')
    if st.button('Anlyze Audio',width='stretch',type='primary'):
        with st.spinner('Process the audio data... '):
            enrolled_res = supabase.table('subject_students').select('*, students(*)').eq('subject_id',subject_code).execute()
            enrolled_student = enrolled_res.data

            if not enrolled_student:
                    st.warning('No Enrolled Student in this subject')
                    return
            candidate_dic ={
                 s['students']['student_id']:s['students']['voice_embedding']
                 for s in enrolled_student if s['students'].get('voice_embedding')
            }

            if not candidate_dic:
                 st.error('No enrolled student have voice profiles register')
                 return
            if audio_data is None:
                st.warning("Please record audio first")
                return
            audio_bytes = audio_data.read()
            # audio_bytes=audio_data.read()

            detected_score = process_bulk(audio_bytes,candidate_dic)
  

            detected_score = {
                    int(k): v
                    for k, v in detected_score.items()
                }
            result,attendance_logs= [], []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            # st.write(type(detected_score))
            # st.write(detected_score)
            for node in enrolled_student:
                        student=node['students']
                        score = detected_score.get(student['student_id'],0.0)
                        is_present = score > 0

                        result.append({
                            "Name": student['name'],
                            "ID":student['student_id'],
                            "source":score if is_present else "_",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_logs=({
                            'student_id':student['student_id'],
                            'subject_id':subject_code,
                            'timestamp':current_timestamp,
                            'is_present':bool(is_present)

                        })
            st.session_state.voice_attendance_result = (pd.DataFrame(result),attendance_logs)
    if st.session_state.get('voice_attendance_result'):
          st.divider()
          df_result, logs = st.session_state.voice_attendance_result

          show_attendance_result(df_result,logs)



    

