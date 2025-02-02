!pip install streamlit matplotlib seaborn

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure Streamlit runs correctly
if __name__ == "__main__":
    # Load the dataset
    @st.cache_data
    def load_data():
        file_path = "/mnt/data/netflix_titles.csv"
        df = pd.read_csv(file_path)
        return df

    df = load_data()

    # Sidebar filters
    st.sidebar.title("Filters")
    year = st.sidebar.selectbox("Select Release Year", options=["All"] + sorted(df["release_year"].dropna().unique(), reverse=True))

    # Apply year filter
    if year != "All":
        df = df[df["release_year"] == int(year)]

    # Title
    st.title("Netflix Data Dashboard")

    # Scatter Plot: Release Year
    st.subheader("Release Year Distribution")
    fig, ax = plt.subplots()
    ax.scatter(df.index, df["release_year"], color="red", alpha=0.5)
    ax.set_title("Scatter Plot of Release Years")
    ax.set_xlabel("Index")
    ax.set_ylabel("Release Year")
    st.pyplot(fig)

    # Bar Chart: Number of Entries Per Country
    st.subheader("Netflix Entries by Country")
    country_counts = df["country"].dropna().str.split(", ").explode().value_counts().head(10)
    fig, ax = plt.subplots()
    country_counts.plot(kind="bar", ax=ax, color="blue")
    ax.set_title("Top 10 Countries by Number of Netflix Entries")
    ax.set_xlabel("Country")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # Donut Chart: Movies vs TV Shows
    st.subheader("Movies vs TV Shows")
    type_counts = df["type"].value_counts()
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%", colors=["lightblue", "lightcoral"], wedgeprops=dict(width=0.4))
    ax.set_title("Movies vs TV Shows")
    st.pyplot(fig)

    # Histogram: Rating Distribution
    st.subheader("Rating Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["rating"].dropna(), bins=10, kde=True, ax=ax, color="purple")
    ax.set_title("Histogram of Ratings")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    st.write("Data Source: Netflix Titles Dataset")
