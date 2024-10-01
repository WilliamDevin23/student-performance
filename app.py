import streamlit as st
import pandas as pd
from inference import predict

st.set_page_config(page_title='Student Performance Prediction')

# Dictionaries
yesno_quest = {1:'Ya', 0:'Tidak'}
gender_dict = {0:'Pria', 1:'Wanita'}
ethnic_dict = {0:'Caucasian', 1:'African American',
               2:'Asian', 3:'Other', 4:'-'}
parent_edu_dict = {0:'Tidak menempuh pendidikan',
                   1:'Sekolah Menengah Atas',
                   2:'Beberapa perkuliahan',
                   3:'Sarjana',
                   4:'Lebih tinggi dari sarjana',
                   5:'-'}

if 'age' not in st.session_state : st.session_state.age = 15
if 'gender' not in st.session_state : st.session_state.gender = 0
if 'ethnic' not in st.session_state : st.session_state.ethnic = 4
if 'parent_edu' not in st.session_state : st.session_state.parent_edu = 5
if 'studytime' not in st.session_state : st.session_state.studytime = 0.0
if 'absences' not in st.session_state : st.session_state.absences = 0
if 'tutor' not in st.session_state : st.session_state.tutor = 0
if 'parentsupport' not in st.session_state : st.session_state.parentsupport = 0
if 'extracur' not in st.session_state : st.session_state.extracur = 0
if 'sport' not in st.session_state : st.session_state.sport = 0
if 'music' not in st.session_state : st.session_state.music = 0
if 'volunteer' not in st.session_state : st.session_state.volunteer = 0
if 'reset_disable' not in st.session_state : st.session_state.reset_disable = True

def format_yn(option) :
    return yesno_quest[option]
    
def format_gender(option) :
    return gender_dict[option]
    
def format_ethnic(option) :
    return ethnic_dict[option]
    
def format_parent_edu(option) :
    return parent_edu_dict[option]

def form_callback() :
    if st.session_state.age_input != st.session_state.age :
        st.session_state.age = st.session_state.age_input

    if st.session_state.gender_input != st.session_state.gender :
        st.session_state.gender = st.session_state.gender_input

    if st.session_state.ethnic_input != st.session_state.ethnic :
        st.session_state.ethnic = st.session_state.ethnic_input

    if st.session_state.parent_edu_input != st.session_state.parent_edu :
        st.session_state.parent_edu = st.session_state.parent_edu_input

    if st.session_state.studytime_input != st.session_state.studytime :
        st.session_state.studytime = st.session_state.studytime_input

    if st.session_state.absences_input != st.session_state.absences :
        st.session_state.absences = st.session_state.absences_input

    if st.session_state.tutor_input != st.session_state.tutor :
        st.session_state.tutor = st.session_state.tutor_input

    if st.session_state.parentsupport_input != st.session_state.parentsupport :
        st.session_state.parentsupport = st.session_state.parentsupport_input

    if st.session_state.extracur_input != st.session_state.extracur :
        st.session_state.extracur = st.session_state.extracur_input

    if st.session_state.sport_input != st.session_state.sport :
        st.session_state.sport = st.session_state.sport_input

    if st.session_state.music_input != st.session_state.music :
        st.session_state.music = st.session_state.music_input

    if st.session_state.volunteer_input != st.session_state.volunteer :
        st.session_state.volunteer = st.session_state.volunteer_input

st.markdown("""
            <style>
                [data-testid="stHorizontalBlock"] > div{
                    height: 300px;
                    overflow: scroll;
                    padding: 10px;
                    border: 1px solid gray;
                    border-radius: 5px;
                }
            </style>
            """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center'>High School Student Performance Prediction</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap='medium')

with col2 :
    st.markdown("<h5 style='text-align: center;'>Orang dengan Karakteristik\
                yang Mirip denganmu Memiliki Grade Berikut</h5>",
                unsafe_allow_html=True)
    grade_container = st.empty()
    with grade_container :
        st.markdown(f"<h1 style='text-align: center; font-size: 88px;'>""</h1>",
                    unsafe_allow_html=True)

with col1 :
    with st.form(key='predict_grade', clear_on_submit=False, border=False) :
        age = st.number_input(label="Berapakah usiamu? (15-18)", min_value=15, key='age_input',
                              max_value=18, step=1, value=st.session_state.age)
        gender = st.radio(label="Apa jenis kelaminmu?", options=[0, 1], key='gender_input',
                          horizontal=True, index=st.session_state.gender,
                          format_func=format_gender)
        ethnic = st.selectbox("Apa etnismu?", list(range(5)), key='ethnic_input',
                              index=st.session_state.ethnic,
                              format_func=format_ethnic)
        parent_edu = st.selectbox(label="Apa pendidikan tertinggi Ayah/Ibumu?", key='parent_edu_input',
                                  options=list(range(6)),
                                  index=st.session_state.parent_edu,
                                  format_func=format_parent_edu)
        studytime = st.number_input(label="Berapa jam lama waktu belajarmu per\
                                    minggu?", min_value=0.0, step=0.1, key='studytime_input',
                                    value=st.session_state.studytime)
        absences = st.number_input(label="Berapa kali kamu absen/tidak hadir di\
                                   kelas dalam setahun terakhir?", key='absences_input',
                                   min_value=0, step=1,
                                   value=st.session_state.absences)
        tutor = st.radio(label="Apakah kamu mengikuti semacam program tutoring?", key='tutor_input',
                         options=[0, 1], horizontal=True,
                         index=st.session_state.tutor,
                         format_func=format_yn)
        parentsupport = st.radio(label="Dari skala 0-4, seberapa besar kamu menilai\
                                 dukungan orang tua terhadap pendidikanmu?", key='parentsupport_input',
                                 options=list(range(5)), horizontal=True,
                                 index=st.session_state.parentsupport)
        extracur = st.radio("Apakah kamu mengikuti kegiatan ekstrakurikuler?",
                            [0, 1], horizontal=True, key='extracur_input',
                            index=st.session_state.extracur,
                            format_func=format_yn)
        sport = st.radio("Apakah kamu aktif dalam kegiatan olah raga?",
                         [0, 1], horizontal=True, key='sport_input',
                         index=st.session_state.sport,
                         format_func=format_yn)
        music = st.radio("Apakah kamu aktif dalam kegiatan musik?",
                         [0, 1], horizontal=True, key='music_input',
                         index=st.session_state.music,
                         format_func=format_yn)
        volunteer = st.radio("Apakah kamu mengikuti kegiatan volunteering?",
                             [0, 1], horizontal=True, key='volunteer_input',
                             index=st.session_state.volunteer,
                             format_func=format_yn)
        
        submit = st.form_submit_button("Submit", on_click=form_callback)
        if submit :
            st.session_state.reset_disable = False
            data = pd.DataFrame({'Age':[age], 'Gender':[gender],
                                 'Ethnicity':[ethnic],
                                 'ParentalEducation':[parent_edu],
                                 'StudyTimeWeekly':[studytime],
                                 'Absences':[absences], 'Tutoring':[tutor],
                                 'ParentalSupport':[parentsupport],
                                 'Extracurricular':[extracur],
                                 'Sports':[sport],
                                 'Music':[music],
                                 'Volunteering':[volunteer]})
            pred = predict(data)
            with col2 :
                with grade_container :
                    st.markdown(f"<h1 style='text-align: center; font-size: 88px;'>{pred}</h1>",
                                unsafe_allow_html=True)
                            
def reset_func() :
    st.session_state.age = 15
    st.session_state.gender = 0
    st.session_state.ethnic = 4
    st.session_state.parent_edu = 5
    st.session_state.studytime = 0.0
    st.session_state.absences = 0
    st.session_state.tutor = 0
    st.session_state.parentsupport = 0
    st.session_state.extracur = 0
    st.session_state.sport = 0
    st.session_state.music = 0
    st.session_state.volunteer = 0
    st.session_state.reset_disable = True

with col2:
    reset = st.button("Reset", disabled=st.session_state.reset_disable,
                      on_click=reset_func)