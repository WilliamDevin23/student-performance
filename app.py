import streamlit as st
import pandas as pd
from inference import predict

st.set_page_config(page_title='Student Performance Prediction')
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

# Dictionaries
yesno_quest = {'Ya':1, 'Tidak':0}
gender_dict = {'Pria':0, 'Wanita':1}
ethnic_dict = {'Caucasian':0, 'African American':1,
               'Asian':2, 'Other':3}
parent_edu_dict = {'Tidak menempuh pendidikan':0,
                   'Sekolah Menengah Atas':1,
                   'Beberapa perkuliahan':2,
                   'Sarjana':3,
                   'Lebih tinggi dari sarjana':4}


col1, col2 = st.columns(2, gap='medium')

with col2 :
    st.markdown("<h3 style='text-align: center;'>Hasil Prediksi Grade Kamu</h3>",
                unsafe_allow_html=True)
    grade_container = st.empty()
    with grade_container :
        st.markdown(f"<h1 style='text-align: center; font-size: 88px;'>""</h1>",
                    unsafe_allow_html=True)

with col1 :
    with st.form(key='predict_grade', clear_on_submit=True, border=False) :
        age = st.number_input(label="Berapakah usiamu? (15-18)", min_value=15,
                              max_value=18, step=1)
        gender = st.radio("Apa jenis kelaminmu?", ['Pria', 'Wanita'],
                          horizontal=True)
        ethnic = st.selectbox("Apa etnismu?", ['African American', 'Asian',
                                               'Caucasian', 'Other'])
        parent_edu = st.selectbox("Apa pendidikan tertinggi Ayah/Ibumu?",
                                  ['Tidak menempuh pendidikan',
                                   'Sekolah Menengah Atas',
                                   'Beberapa perkuliahan',
                                   'Sarjana',
                                   'Lebih tinggi dari sarjana'])
        studytime = st.number_input(label="Berapa jam lama waktu belajarmu per\
                                    minggu?",
                                    min_value=0.0, step=0.1)
        absences = st.number_input(label="Berapa kali kamu absen/tidak hadir di\
                                   kelas dalam setahun terakhir?",
                                   min_value=0, step=1)
        tutor = st.radio("Apakah kamu mengikuti semacam program tutoring?",
                         ['Ya', 'Tidak'], horizontal=True)
        parentsupport = st.radio("Dari skala 0-4, seberapa besar kamu menilai\
                                 dukungan orang tua terhadap pendidikanmu?",
                                 [0, 1, 2, 3, 4], horizontal=True)
        extracur = st.radio("Apakah kamu mengikuti kegiatan ekstrakurikuler?",
                            ['Ya', 'Tidak'], horizontal=True)
        sport = st.radio("Apakah kamu aktif dalam kegiatan olah raga?",
                         ['Ya', 'Tidak'], horizontal=True)
        music = st.radio("Apakah kamu aktif dalam kegiatan musik?",
                         ['Ya', 'Tidak'], horizontal=True)
        volunteer = st.radio("Apakah kamu mengikuti kegiatan volunteering?",
                             ['Ya', 'Tidak'], horizontal=True)
        if st.form_submit_button("Submit") :
            print(gender_dict[gender])
            data = pd.DataFrame({'Age':[age], 'Gender':[gender_dict[gender]],
                                 'Ethnicity':[ethnic_dict[ethnic]],
                                 'ParentalEducation':[parent_edu_dict[parent_edu]],
                                 'StudyTimeWeekly':[studytime],
                                 'Absences':[absences], 'Tutoring':[yesno_quest[tutor]],
                                 'ParentalSupport':[parentsupport],
                                 'Extracurricular':[yesno_quest[extracur]],
                                 'Sports':[yesno_quest[sport]],
                                 'Music':[yesno_quest[music]],
                                 'Volunteering':[yesno_quest[volunteer]]})
            pred = predict(data)
            with col2 :
                with grade_container :
                    st.markdown(f"<h1 style='text-align: center; font-size: 88px;'>{pred}</h1>",
                                unsafe_allow_html=True)
                            
with col2:
    reset = st.button("Reset")