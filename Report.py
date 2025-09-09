
import streamlit as st

# Increase upload file limit to 500MB
st.set_option("server.maxUploadSize", 500)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Data Report Generator", layout="wide")

# Page Title
st.title("📊 Data Report Generator")

# File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV
    x = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Summary Statistics
    st.subheader("🔍 Summary Statistics")
    st.dataframe(x.describe(include='all').transpose())

    # Missing Value Report
    st.subheader("❗ Missing Value Report")
    missing = x.isnull().sum()
    st.dataframe(missing[missing > 0])

    # Histograms for Numerical Data
    st.subheader("📊 Histograms for Numerical Data")
    sns.set_style("whitegrid")
    numeric_cols = x.select_dtypes(include='number').columns

    for col in numeric_cols:
        st.markdown(f"**{col}**")
        fig, ax = plt.subplots(figsize=(5, 3), dpi=80)
        sns.histplot(x[col].dropna(), kde=True, ax=ax, color='skyblue', edgecolor='black')
        ax.set_title(f"Distribution of {col}", fontsize=10)
        ax.set_xlabel(col, fontsize=9)
        ax.set_ylabel("Frequency", fontsize=9)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=False)

    # Correlation Matrix
    st.subheader("🔗 Correlation Matrix")
    corr = x[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(6, 4), dpi=80)
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5,
                linecolor='white', ax=ax, annot_kws={"size": 7})
    ax.set_title("Correlation Heatmap", fontsize=10)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=False)

    # Footer Info
    st.info("✅ All reports have been generated based on your uploaded CSV file.")

else:
    st.warning("👈 Please upload a CSV file to get started.")
