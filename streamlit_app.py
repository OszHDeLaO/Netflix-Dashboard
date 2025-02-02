import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load the dataset (cached for performance)
@st.cache_data  
def load_data():
    file_path = "netflix_titles.csv"  # Update with your file path if needed
    df = pd.read_csv(file_path)
    return df

# Main function to create the Streamlit app
def main():
    # Load the dataset
    df = load_data()

    # Sidebar filters
    st.sidebar.title("Filters")
    year = st.sidebar.selectbox("Select Release Year", options=["All"] + sorted(df["release_year"].dropna().unique(), reverse=True))
    
    # Theme mapping for color scales
    theme_mapping = {
        "Plotly": "plotly3",
        "Seaborn": "icefire",
        "Viridis": "viridis",
        "Blackbody": "blackbody",
        "Cividis": "cividis"
    }
    theme = st.sidebar.selectbox("Select Color Theme", options=list(theme_mapping.keys()))

    # Apply year filter
    if year != "All":
        df = df[df["release_year"] == int(year)]

    # Title of the dashboard
    st.title("Netflix Data Dashboard")

    # Scatter Plot: Release Year Distribution
    st.subheader("Release Year Distribution")
    fig_scatter = px.scatter(df, x=df.index, y="release_year", title="Scatter Plot of Release Years", color_discrete_sequence=["red"])
    st.plotly_chart(fig_scatter)

    # World Map: Number of Entries Per Country
    st.subheader("Netflix Entries by Country")
    country_counts = df["country"].dropna().str.split(", ").explode().value_counts().reset_index()
    country_counts.columns = ["Country", "Count"]
    fig_map = px.choropleth
