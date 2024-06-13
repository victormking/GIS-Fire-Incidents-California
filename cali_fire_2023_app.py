import streamlit as st
import pandas as pd
import pydeck as pdk

# Function to load and preprocess data
def load_data():
    data = pd.read_csv('fire_in_california.csv')
    data['acq_date'] = pd.to_datetime(data['acq_date'])
    data['month'] = data['acq_date'].dt.month_name()
    return data

# Load data
data = load_data()

# Streamlit app
st.title('Fire Incidents in California')

# Dropdown to select month
month_list = data['month'].unique()
selected_month = st.selectbox('Select a Month', month_list)

# Filter data based on selected month
filtered_data = data[data['month'] == selected_month]

# Display map with tooltips
if not filtered_data.empty:
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=filtered_data['latitude'].mean(),
            longitude=filtered_data['longitude'].mean(),
            zoom=6,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=filtered_data,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=5000,
                pickable=True,  # Make layers pickable to enable tooltips
                auto_highlight=True
            ),
        ],
        tooltip={
            "html": "<b>Fire Info:</b><br>Latitude: {latitude}<br>Longitude: {longitude}<br>Date: {acq_date}",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white"
            }
        }
    ))
else:
    st.write('No data available for the selected month.')
