import streamlit as st
import pandas as pd
import pickle
from project import predict_heart_disease

page_bg_img = '''
<style>

h1 {
    color: #ffffff; /* Darker color for headings */
    text-align: center;
    font-family: 'Arial', sans-serif;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    width: 100%;
    font-size: 16px;
}

.stButton>button:hover {
    background-color: #45a049;
}

.stTextInput>div>div>input {
    background-color: #f1f1f1;
    border: 2px solid #ccc;
    color: black;
}

.stSelectbox>div>div>div {
    background-color: #f1f1f1;
    border: 2px solid #ccc;
    color: black;
}

.stAlert {
    background-color: #000000; /* White background for alerts */
    border-radius: 10px;
    padding: 10px;
    font-size: 16px;
    margin-top: 10px;
    color: #ffffff; /* Black color for output text */
}

</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title('Heart Failure Prediction')

# Collect user input data
age = st.number_input('Age', min_value=0, max_value=120, value=50)
sex = st.selectbox('Sex', ('Male', 'Female'))
chest_pain = st.selectbox('Chest Pain Type', ('Typical Angina', 'Atypical Angina', 'Non-Anginal Pain', 'Asymptomatic'))
resting_bp = st.number_input('Resting Blood Pressure (mm Hg)', min_value=0, max_value=250, value=120)
cholesterol = st.number_input('Cholesterol (mg/dl)', min_value=0, max_value=600, value=200)
fasting_bs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', ('Yes', 'No'))
resting_ecg = st.selectbox('Resting ECG', ('Normal', 'ST-T wave abnormality', 'Left ventricular hypertrophy'))
max_hr = st.number_input('Max Heart Rate Achieved', min_value=0, max_value=250, value=150)
exercise_angina = st.selectbox('Exercise-Induced Angina', ('Yes', 'No'))
oldpeak = st.number_input('ST Depression', min_value=0.0, max_value=10.0, value=1.0)
st_slope = st.selectbox('Slope of the ST Segment', ('Upsloping', 'Flat', 'Downsloping'))

# Map input values to encoded variables
sex = 1 if sex == 'Male' else 0
chest_pain_map = {'Asymptomatic': 3, 'Atypical Angina': 2, 'Non-Anginal Pain': 1, 'Typical Angina': 0}
resting_ecg_map = {'Left ventricular hypertrophy': 2, 'Normal': 1, 'ST-T wave abnormality': 0}
exercise_angina = 1 if exercise_angina == 'Yes' else 0
st_slope_map = {'Downsloping': 2, 'Flat': 1, 'Upsloping': 0}

# Create a DataFrame for user input
user_input = pd.DataFrame({
    'Age': [age],
    'Sex': [sex],
    'ChestPainType': [chest_pain_map[chest_pain]],
    'RestingBP': [resting_bp],
    'Cholesterol': [cholesterol],
    'FastingBS': [1 if fasting_bs == 'Yes' else 0],
    'RestingECG': [resting_ecg_map[resting_ecg]],
    'MaxHR': [max_hr],
    'ExerciseAngina': [exercise_angina],
    'Oldpeak': [oldpeak],
    'ST_Slope': [st_slope_map[st_slope]]
})

# Predict using the loaded model
if st.button('Predict'):
    prediction = predict_heart_disease(user_input)
    if prediction == 1:
        st.error('⚠️ The model predicts a **high risk** of heart disease.', icon="⚠️")
    else:
        st.success('✅ The model predicts a **low risk** of heart disease.', icon="✅")
