import streamlit as st
import pickle
import numpy as np
import os

def load_model():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'saved_steps.pkl')
    
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

# Try to load the model, handle file not found error
try:
    data = load_model()
    regressor = data["model"]
    le_country = data["le_country"]
    le_education = data["le_education"]
except FileNotFoundError as e:
    st.error(str(e))
    regressor = None
    le_country = None
    le_education = None

def show_predict_page():
    if regressor is None or le_country is None or le_education is None:
        st.error("Model or Label Encoders are not loaded properly. Please check the file.")
        return
    
    st.title("Software Developer Salary Prediction")
    st.write("""### We need some information to predict the salary""")

    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
