
import pandas as pd
import altair as alt

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

    # Apply year filter
    if year != "All":
        df = df[df["release_year"] == int(year)]

    # Title of the dashboard
    st.title("Netflix Data Dashboard (Simplified)")

    # 1. Bar Chart: Top 10 Countries with Most Content
    st.subheader("Top 10 Countries with Most Content")
    top_countries = df["country"].value_counts().head(10)
    st.bar_chart(top_countries)  # Streamlit's built-in bar chart

    # 2. Line Chart: Number of Releases Over Time
    st.subheader("Number of Releases Over Time")
    releases_over_time = df.groupby("release_year")["show_id"].count().reset_index()
    st.line_chart(releases_over_time.set_index("release_year"))  # Streamlit's built-in line chart

    # 3. Pie Chart: Movies vs. TV Shows
    st.subheader("Movies vs. TV Shows")
    type_counts = df["type"].value_counts()
    st.pie_chart(type_counts)  # Streamlit's built-in pie chart

    # 4. Area Chart: Distribution of Ratings
    st.subheader("Distribution of Ratings")
    rating_counts = df["rating"].value_counts().sort_index()
    st.area_chart(rating_counts)  # Streamlit's built-in area chart
  
    # Data Source
    st.write("Data Source: Netflix Titles Dataset")

# Entry point for the script
if __name__ == "__main__":
    main()
