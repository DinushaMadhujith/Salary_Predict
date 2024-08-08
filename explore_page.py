import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.mosaicplot import mosaic

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
        ### Stack Overflow Developer Survey 2020
        """
    )

    # Mosaic Chart
    st.write(
        """
        #### Mosaic Chart of Salary by Education Level and Country
        """
    )

    mosaic_data = df.groupby(['Country', 'EdLevel']).size().reset_index(name='Count')
    mosaic_data = mosaic_data.pivot(index='Country', columns='EdLevel', values='Count').fillna(0)

    fig1, ax1 = plt.subplots(figsize=(12, 8))
    mosaic(mosaic_data.stack(), gap=0.01, title='Mosaic Chart of Salary by Education Level and Country', ax=ax1)

    st.pyplot(fig1)

    # Scatter Plot
    st.write(
        """
        #### Scatter Plot of Salary vs. Years of Experience
        """
    )

    fig2, ax2 = plt.subplots()
    ax2.scatter(df["YearsCodePro"], df["Salary"], alpha=0.5)
    ax2.set_xlabel("Years of Experience")
    ax2.set_ylabel("Salary")
    ax2.set_title("Scatter Plot of Salary vs. Years of Experience")

    st.pyplot(fig2)

    # Bar Chart
    st.write(
        """
        #### Mean Salary Based On Country
        """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    # Line Chart
    st.write(
        """
        #### Mean Salary Based On Experience
        """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
