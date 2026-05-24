from src.database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()
def check_pass(pwd,hashed):
    # return bcrypt.hashpw(pwd.encode(),hashed.encode())
    return bcrypt.checkpw(
        pwd.encode(),
        hashed.encode()
    )
def check_teacher_exist(username):

    response = supabase.table('teachers').select('username').eq('username',username).execute()

    return len(response.data) > 0

def create_teacher(username,password,name):

    data = {'username':username,'password':hash_pass(password),"name":name}
    response = supabase.table('teachers').insert(data).execute()

    return response.data

def teacher_login(username,password):
    response = supabase.table('teachers').select("*").eq('username',username).execute()
    if response.data:
        teacher= response.data[0]
        if check_pass(password,teacher['password']):
            return teacher
    return None

def get_all_students():
    response = supabase.table('students').select('*').execute()
    return response.data

def create_student(new_name, face_emb=None, voice_emb=None):
    data = {'name':new_name,'face_embedding': face_emb,'voice_embedding':voice_emb}
    response = supabase.table('students').insert(data).execute()
    return response.data

def create_subject(sub_id,sub_name,sub_section,teacher_id):
    data = {'subject_code':sub_id,'name':sub_name,'section':sub_section,'teacher_id':teacher_id}
    response = supabase.table('subjects').insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response = supabase.table('subjects').select("* , subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id). execute()
    subjects = response.data
    # print(subjects)

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}]) [0].get('count', 0) if sub.get('subject_students')else 0
        attendance = sub.get('attendance_logs',[])
        unique_session = len(set(log['timestamp'] for log in attendance))

        sub['total_classes'] = unique_session

        sub.pop('subject_students',None)
        sub.pop('attendance_logs',None)

    return subjects

def enroll_student_to_subject(student_id, subject_id):
    data = {'subject_id':subject_id,'student_id':student_id}
    res = supabase.table('subject_students').insert(data).execute()
    return res.data
def unenroll_student_to_subject(student_id, subject_id):
    res = supabase.table('subject_students').delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()

    return res.data

def get_enrolled_subject(student_id):
    res = supabase.table('subject_students').select('*, subjects(*)').eq('student_id',student_id).execute()
    return res.data

def get_student_attendance(student_id):
    # res = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id',student_id).execute()
    res = supabase.table('attendance_logs').select('*').eq('student_id',student_id).execute()
    return res.data

def create_attendance(logs):

    res = supabase.table('attendance_logs').insert(logs).execute()
    return res.data

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id',teacher_id).execute()
    return response.data