import streamlit as st
import pandas as pd
import plotly.express as px

# Ensure Streamlit runs correctly
if __name__ == "__main__":
    # Load the dataset
    @st.cache_data
    def load_data():
        file_path = "netflix_titles.csv"  # Update with your file path if needed
        df = pd.read_csv(file_path)
        return df

    df = load_data()

    # Sidebar filters
    st.sidebar.title("Filters")
    year = st.sidebar.selectbox("Select Release Year", options=["All"] + sorted(df["release_year"].dropna().unique(), reverse=True))
    
    # Theme mapping (fix for the colorscale issue)
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

    # Title
    st.title("Netflix Data Dashboard")

    # Scatter Plot: Release Year
    st.subheader("Release Year Distribution")
    fig_scatter = px.scatter(df, x=df.index, y="release_year", title="Scatter Plot of Release Years", color_discrete_sequence=["red"])
   

    # World Map: Number of Entries Per Country
    st.subheader("Netflix Entries by Country")
    country_counts = df["country"].dropna().str.split(", ").explode().value_counts().reset_index()
    country_counts.columns = ["Country", "Count"]
    fig_map = px.choropleth(country_counts, locations="Country", locationmode="country names", color="Count",
                             color_continuous_scale=theme_mapping[theme], title="Number of Netflix Entries by Country")  # Use theme_mapping
    st.plotly_chart(fig_map)

    # Donut Chart: Movies vs TV Shows
    st.subheader("Movies vs TV Shows")
    type_counts = df["type"].value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]
    fig_pie = px.pie(type_counts, values="Count", names="Type", hole=0.4, title="Movies vs TV Shows",
                     color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_pie)

    # Histogram: Rating Distribution
    st.subheader("Rating Distribution")
    fig_hist = px.histogram(df, x="rating", title="Histogram of Ratings", color_discrete_sequence=["blue"])
    st.plotly_chart(fig_hist)

    st.write("Data Source: Netflix Titles Dataset")  # Update if needed
