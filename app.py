import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Title and description
st.title("Spanish Civil War (1936-1938) Map")
st.markdown("""
This app visualizes the progression of the Spanish Civil War (1936-1938) on a map.  
Use the slider to explore daily changes during the war.
""")

# Load event data
@st.cache_data
def load_data():
    # Example dataset: Replace with actual war data
    # The dataset should include date, location (lat/lon), type of event, and descriptions
    data = pd.read_csv("spanish_civil_war_data.csv")
    return data

# Load geospatial data (shapefile)
@st.cache_data
def load_shapefile():
    shapefile_path = "data/spain_boundaries.shp"  # Update path to your shapefile
    gdf = gpd.read_file(shapefile_path)
    return gdf

# Load the data
data = load_data()

# Select a date to view
min_date, max_date = pd.to_datetime(data["date"]).min(), pd.to_datetime(data["date"]).max()
selected_date = st.slider("Select a date", min_date, max_date, min_date)

# Filter data by selected date
filtered_data = data[data["date"] == selected_date.strftime("%Y-%m-%d")]

# Load the shapefile (geospatial data)
gdf = load_shapefile()

# Map initialization
m = folium.Map(location=[40.0, -3.7], zoom_start=6)

# Add the shapefile data (boundaries of Spain)
folium.GeoJson(gdf).add_to(m)

# Add events to the map
for _, row in filtered_data.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"<strong>{row['event_type']}</strong>: {row['description']}",
        icon=folium.Icon(color="red" if row["side"] == "Republican" else "blue")
    ).add_to(m)

# Render map
st_data = st_folium(m, width=700, height=500)

# Sidebar information
st.sidebar.header("About the App")
st.sidebar.markdown("""
- **Visualization:** Interactive map to explore daily changes.
- **Data:** Historical records of battles, territorial changes, and key events.
""")
