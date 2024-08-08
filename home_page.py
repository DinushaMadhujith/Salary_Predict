import streamlit as st

def show_home_page():
    st.title("Welcome to the Software Developer Salary App")

    st.write(
        """
        ## About This App

        This application allows you to explore and predict software developer salaries based on various factors such as country, education level, and years of experience.

        ### Pages

        - **Home:** This page, providing an overview of the app.
        - **Explore:** Explore software developer salaries based on data from the Stack Overflow Developer Survey.
        - **Predict:** Predict the salary of a software developer based on input factors.

        ### Instructions

        Use the sidebar to navigate between the pages. On the "Explore" page, you can view various visualizations of the salary data. On the "Predict" page, you can input your information to get an estimated salary prediction.

        ### Data Source

        The data used in this application is from the Stack Overflow Developer Survey.
        """
    )

    # Optional: Display an image if needed
    image_path = r'C:\Dinusha\predict_salary\salary\salary\download.jpg'
    st.image(image_path, caption='Stack Overflow Developer Survey 2020', use_column_width=True)
