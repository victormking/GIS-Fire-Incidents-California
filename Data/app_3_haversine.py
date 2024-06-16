import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Load data
def load_data():
    data = pd.read_csv('fire_in_california.csv')
    data['acq_date'] = pd.to_datetime(data['acq_date'])
    data['month'] = data['acq_date'].dt.month_name()
    return data

# Haversine formula to calculate distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in km
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    distance = R * c
    return distance

# Calculate distances between all pairs of fires
def calculate_distances(data):
    distances_list = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            lat1, lon1 = data.iloc[i]['latitude'], data.iloc[i]['longitude']
            lat2, lon2 = data.iloc[j]['latitude'], data.iloc[j]['longitude']
            distance = haversine(lat1, lon1, lat2, lon2)
            distances_list.append({'fire1': i, 'fire2': j, 'distance': distance})
    return pd.DataFrame(distances_list)

# Streamlit app
st.title('Fire Incidents in California')
data = load_data()

# Calculate distances
distances = calculate_distances(data)

# Display statistics
st.subheader('Distance Statistics')
st.write('Total number of fires:', len(data))
st.write('Shortest distance between fires:', distances['distance'].min(), 'km')
st.write('Longest distance between fires:', distances['distance'].max(), 'km')
st.write('Average distance between fires:', distances['distance'].mean(), 'km')

# Plotting the map
st.subheader('Fire Locations')
if not data.empty:
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=data['latitude'].mean(),
            longitude=data['longitude'].mean(),
            zoom=6,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=data,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=5000,
            ),
            pdk.Layer(
                'LineLayer',
                data=distances,
                get_source_position='[data.iloc[fire1]["longitude"], data.iloc[fire1]["latitude"]]',
                get_target_position='[data.iloc[fire2]["longitude"], data.iloc[fire2]["latitude"]]',
                get_color=[0, 0, 255],
                get_width=5,
            )
        ],
    ))
else:
    st.write('No data available for the selected month.')
