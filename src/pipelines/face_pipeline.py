import numpy as np
from sklearn.svm import SVC
import face_recognition_models
import dlib
import streamlit as st
from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_face_embedding(img_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(img_np,1)
    embeddings = []

    for face in faces:
        shape = sp(img_np,face)
        face_descriptor = facerec.compute_face_descriptor(img_np,shape,1)

        embeddings.append(np.array(face_descriptor))

    return embeddings
@st.cache_resource
def get_trained_model():
    x = []
    y = []

    students_db = get_all_students()
    if not students_db:
        return None
    for student in students_db:
        embedding = student.get('face_embedding')
        if embedding:
            x.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(x) == 0:
        return 0
    unique_classes = set(y)
    if len(unique_classes) < 2:
        # st.warning("Need at least 2 students to train model")
        return None
    clf = SVC(kernel='linear',probability=True, class_weight='balanced')

    try:
        clf.fit(x,y)
    except Exception as e:
        st.error('traing failed',e)

    return {'clf':clf,'x':x,'y':y}
def trained_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

    
def predict_attendance(img):
    encodings = get_face_embedding(img)

    detected_student = {}

    model_data = get_trained_model()
    if model_data is None:
        # st.warning("Model not trained yet")
        return detected_student,[], len(encodings)
    
    clf = model_data['clf']
    x_train = model_data['x']
    y_train = model_data['y']


    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        if len(encoding)>=2:
            predicted_id =int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        # student_embeddings= x_train(y_train.index('predicted_id'))
        student_embeddings = x_train[y_train.index(predicted_id)]

        best_match_score = np.linalg.norm(student_embeddings-encoding)
        threshold = 0.6
        if best_match_score <= threshold:
            detected_student[predicted_id] = True

    return detected_student, all_students, len(encodings)


