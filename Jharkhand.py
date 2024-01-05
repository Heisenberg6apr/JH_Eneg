import streamlit as st
import pandas as pd
import folium
import json
from streamlit_folium import folium_static
from streamlit_folium import st_folium


# Set Streamlit page title and header
st.set_page_config(page_title='Renewable Energy Dashboard')
st.title('RE Installation Count and Capacity Visualization in the State of Jharkhand')

# Read the CSV data
dfall = pd.read_csv('UPdated from JREDA/All_Total.csv')

# Load GeoJSON data
with open('UPdated from JREDA/jhnew.geojson') as f:
    geojson_data = json.load(f)

st.subheader('Hover over the Districts to get the Total Count and Capacity in Jharkhand')

# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.8,
    }

# Function to filter data based on selected district
def filter_data_by_district(district):
    if district == 'Jharkhand':
        return dfall  # Return the entire DataFrame for Jharkhand
    else:
        filtered_dfall = dfall[dfall['District'] == district]
        return filtered_dfall
    
# Sidebar district selection
districts = ['Jharkhand'] + dfall['District'].unique().tolist()  # Add 'Jharkhand' to the list of districts
selected_district = st.sidebar.selectbox('Select a District to get all details of Installations', districts)

# Filter data based on selected district
filtered_dfall = filter_data_by_district(selected_district)

m = folium.Map(location=[23.6345, 85.3803], zoom_start=7,min_zoom=5, max_zoom=15, tiles='cartodb dark_matter', control_scale=True)
folium.TileLayer('cartodbpositron', name='Light Map').add_to(m)  # Add light map layer
folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['dtname','State_Solar_Counts','State_Solar_Capacity','State_Solarpump_counts','State_solarMinigrid_Plant_capacity','State_SolarGrid_mini_plant','SGM_count','SGM_Capacity','Solar_streetlights'], 
                                 aliases=['District:','Grid Connected installed Solar Rooftop Counts(No.)','Grid Connected Solar Rooftop Capacity(kWp)','Solar Pump Counts(No.)','Minigrid Solar Capacity(kWp)','Minigrid Solar installed Counts(No.)','Solar Ground Mounted Counts(No.)','Solar Ground Mounted Capacity(Kwp)','Solar street lights Count(No.)'])
).add_to(m)

# Lock the zoom level
m.options['scrollWheelZoom'] = False

folium.LayerControl().add_to(m)

folium_static(m, width=700, height=500)

# Calculate metrics from filtered data
sum_households = filtered_dfall['Count_Solar_Mini_Grid_Plant'].sum()
sum_minigrid_capacity = filtered_dfall['Capacity_Solar_Mini_Grid_Plant'].sum()
sum_sgmp_capacity = filtered_dfall['SGM_Capacity'].sum()
sum_rooftop_capacity = filtered_dfall['Grid_Connected_Rooftop_Solar_Capacity_Installed_(in_KWp)'].sum()
sum_rooftop_installations = filtered_dfall['Total_Number_of_Building_solar_rooftop_grid_connected'].sum()
sum_solar_pumps = filtered_dfall['Count_solar_pump_installed'].sum()
sum_private_rooftop_installations = filtered_dfall['Privatesolar'].sum()
sum_utility_Grade_Solar = filtered_dfall['SGM_Capacity'].sum()
sum_privatesolar_counts=filtered_dfall['private_solar_count'].sum()


# Display metrics
st.header('State Owned')
st.metric(label=' ', value=selected_district)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Rooftop Solar Capacity (kWp)", value=sum_rooftop_capacity)
with col2:
    st.metric(label="Minigrid capacity(kWp)", value=sum_minigrid_capacity)
with col3:
    st.metric(label="Solar Water Pumps", value=sum_solar_pumps)

col4, col5 = st.columns(2)
with col4:
    st.metric(label="Rooftop Solar Installations", value=sum_rooftop_installations)
with col5:
    st.metric(label="Installed Minigrid Solar(No.)", value = sum_households)


st.header('Private Owned')

col7, col8, col9,col10 = st.columns(4)
with col7:
    st.metric(label="RooftopsolarCapacity(kWp)", value=sum_private_rooftop_installations)
with col8:
    st.metric(label="Solar Water Pumps", value=sum_solar_pumps)
with col9:
    st.metric(label="Utility Grade Solar cap(kWp)", value=sum_utility_Grade_Solar)

with col10:
    st.metric(label="Rooftop Solar Nos.", value=sum_privatesolar_counts)

