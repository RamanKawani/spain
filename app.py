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

# Load data
@st.cache
def load_data():
    # Example dataset: Replace with actual war data (CSV with lat, lon, and event details)
    data = pd.read_csv("spanish_civil_war_data.csv")
    return data

# GeoPandas: Load shapefile (replace with actual shapefile of Spain, if necessary)
@st.cache
def load_shapefile():
    shapefile_path = "path_to_shapefile/spain_boundaries.shp"  # Replace with correct path
    gdf = gpd.read_file(shapefile_path)
    return gdf

# Load geospatial data
gdf = load_shapefile()

# Load event data
data = load_data()

# Select a date to view
min_date, max_date = pd.to_datetime(data["date"]).min(), pd.to_datetime(data["date"]).max()
selected_date = st.slider("Select a date", min_date, max_date, min_date)

# Filter data by selected date
filtered_data = data[data["date"] == selected_date.strftime("%Y-%m-%d")]

# Map initialization
m = folium.Map(location=[40.0, -3.7], zoom_start=6)

# Add Spain boundaries from shapefile (GeoPandas)
folium.GeoJson(
    gdf.to_crs("EPSG:4326"),  # Ensure the coordinate reference system is correct
    name="Spain Boundaries",
    style_function=lambda x: {
        "fillColor": "green",
        "color": "black",
        "weight": 0.5,
        "fillOpacity": 0.2,
    },
).add_to(m)

# Add events to the map
for _, row in filtered_data.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"<strong>{row['event_type']}</strong>: {row['description']}",
        icon=folium.Icon(color="red" if row["side"] == "Republican" else "blue")
    ).add_to(m)

# Render map in Streamlit
st_data = st_folium(m, width=700, height=500)

# Sidebar information
st.sidebar.header("About the App")
st.sidebar.markdown("""
- **Visualization:** Interactive map to explore daily changes.
- **Data:** Historical records of battles, territorial changes, and key events.
""")
