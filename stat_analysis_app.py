import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set the page configuration
st.set_page_config(
    page_title="Statistical Analysis and EDA App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Main title of the app
st.title("📊 Statistical Analysis and Exploratory Data Analysis (EDA) App")

# Description of the app
st.markdown("""
Welcome to the Statistical Analysis and EDA App! This tool allows you to upload your dataset, 
perform exploratory data analysis, and create various statistical plots interactively.

**Instructions:**
1. Upload your dataset in CSV or Excel format.
2. Choose the type of analysis or plot you want to perform.
3. Customize the plots according to your preferences.
""")

# Function to upload and read dataset
def upload_data():
    st.sidebar.header("Upload Dataset")
    uploaded_file = st.sidebar.file_uploader("Upload your file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            st.sidebar.success("File uploaded successfully!")
            return df
        except Exception as e:
            st.sidebar.error(f"Error: {e}")
    return None

# Function to display EDA
def display_eda(df):
    st.header("Exploratory Data Analysis (EDA)")
    
    if st.checkbox('Show dataframe'):
        st.subheader("Dataframe")
        st.write(df)
    
    if st.checkbox('Show summary statistics'):
        st.subheader("Summary Statistics")
        st.write(df.describe())

    if st.checkbox('Show correlation matrix'):
        st.subheader("Correlation Matrix")
        # Filter out non-numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            st.warning("No numeric columns available for correlation matrix.")
        else:
            corr = numeric_df.corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
    
    if st.checkbox('Show pair plot'):
        st.subheader("Pair Plot")
        # Filter out non-numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            st.warning("No numeric columns available for pair plot.")
        else:
            fig = sns.pairplot(numeric_df)
            st.pyplot(fig)

# Function to display statistical plots
def display_plots(df):
    st.header("Statistical Plots")

    plot_type = st.selectbox("Select plot type", ["Scatter Plot", "Line Plot", "Bar Plot", "Histogram", "Box Plot"], key="plot_type")

    all_columns = df.columns.tolist()
    x_axis = st.selectbox("Select X-axis", all_columns, key="x_axis")
    y_axis = st.selectbox("Select Y-axis", all_columns, key="y_axis")

    if plot_type == "Scatter Plot":
        fig = px.scatter(df, x=x_axis, y=y_axis)
    elif plot_type == "Line Plot":
        fig = px.line(df, x=x_axis, y=y_axis)
    elif plot_type == "Bar Plot":
        fig = px.bar(df, x=x_axis, y=y_axis)
    elif plot_type == "Histogram":
        fig = px.histogram(df, x=x_axis)
    elif plot_type == "Box Plot":
        fig = px.box(df, x=x_axis, y=y_axis)
    
    st.plotly_chart(fig)

# Main function to run the app
def main():
    df = upload_data()
    if df is not None:
        st.sidebar.header("Choose Analysis")
        analysis_type = st.sidebar.radio("Select Analysis Type", ["EDA", "Statistical Plots"])

        if analysis_type == "EDA":
            display_eda(df)
        elif analysis_type == "Statistical Plots":
            display_plots(df)
    else:
        st.info("Please upload a dataset using the sidebar.")

if __name__ == "__main__":
    main()
