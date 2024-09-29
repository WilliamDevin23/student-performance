import pickle
import tensorflow as tf
import streamlit as st
import numpy as np

@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('student_prediction.h5')
    return model

@st.cache_resource
def load_scaler():
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return scaler

@st.cache_data(ttl=3600)
def predict(data) :
    class_dict = {0:'A', 1:'B', 2:'C',
                  3:'D', 4:'E'}
    model = load_model()
    scaler = load_scaler()
    data = scaler.transform(data)
    pred = model.predict(data)
    pred_class = np.argmax(pred, axis=-1)[0]
    return class_dict[pred_class]