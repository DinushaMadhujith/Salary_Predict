import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page
from home_page import show_home_page  

# Default page is "Home"
page = st.sidebar.selectbox("Navigation", ("Home", "Predict", "Explore"), index=0)

# Show the page based on the sidebar selection
if page == "Home":
    show_home_page()
elif page == "Predict":
    show_predict_page()
elif page == "Explore":
    show_explore_page()
