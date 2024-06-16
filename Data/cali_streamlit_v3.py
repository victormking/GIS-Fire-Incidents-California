import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from datetime import datetime
from haversine import haversine, Unit

# Load data
def load_data():
    data = pd.read_csv('fire_in_california.csv')
    data['acq_date'] = pd.to_datetime(data['acq_date'])
    data['month'] = data['acq_date'].dt.month_name()
    return data

# Haversine formula to calculate distance
def haversine_distance(lat1, lon1, lat2, lon2):
    return haversine((lat1, lon1), (lat2, lon2))

# Calculate distances between all pairs of fires
def calculate_distances(data):
    distances_list = []
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            lat1, lon1 = data.iloc[i]['latitude'], data.iloc[i]['longitude']
            lat2, lon2 = data.iloc[j]['latitude'], data.iloc[j]['longitude']
            distance = haversine_distance(lat1, lon1, lat2, lon2)
            distances_list.append({'fire1': i, 'fire2': j, 'distance': distance})
    return pd.DataFrame(distances_list)

# Streamlit app
st.title('Fire Incidents in California')

data = load_data()
distances = calculate_distances(data)

# Display statistics
st.sidebar.title("Distance Statistics")
st.sidebar.write(f"Total number of fires: {len(data)}")
st.sidebar.write(f"Shortest distance between fires: {distances['distance'].min()} km")
st.sidebar.write(f"Longest distance between fires: {distances['distance'].max()} km")
st.sidebar.write(f"Average distance between fires: {distances['distance'].mean()} km")

# Plot the map with Pydeck
st.header('Fire Locations')

scatter_layer = pdk.Layer(
    'ScatterplotLayer',
    data,
    get_position='[longitude, latitude]',
    get_color='[200, 30, 0, 160]',
    get_radius=5000,
    pickable=True
)

tooltip = {
    "html": "<b>Fire Date:</b> {acq_date}<br><b>Latitude:</b> {latitude}<br><b>Longitude:</b> {longitude}",
    "style": {"color": "white"}
}

r = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=data['latitude'].mean(),
        longitude=data['longitude'].mean(),
        zoom=6,
        pitch=50,
    ),
    layers=[scatter_layer],
    tooltip=tooltip
)

st.pydeck_chart(r)

# Interactive distance calculation
st.header("Calculate Distance Between Fires")
st.write("Enter the coordinates of two fires to calculate the distance between them.")

with st.form(key='distance_form'):
    lat1 = st.number_input("Latitude of Fire 1")
    lon1 = st.number_input("Longitude of Fire 1")
    lat2 = st.number_input("Latitude of Fire 2")
    lon2 = st.number_input("Longitude of Fire 2")
    submit_button = st.form_submit_button(label='Calculate Distance')

if submit_button:
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    st.write(f"Distance between selected points: {distance:.2f} km")
