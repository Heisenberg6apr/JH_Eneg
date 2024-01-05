import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import folium
import plotly.express as px
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import json
import openpyxl

dfST=pd.read_excel("UPdated from JREDA/SSL compiled report.xlsx")



with open(r"C:\Users\sachi\OneDrive\Desktop\webapp\data\JHARKHANDSHAPEFILEGJ.geojson") as f:
        geojson_data = json.load(f)


polygon_shapefile = "UPdated from JREDA\private owned solar rooftop\JHARKHAND_DISTRICT_BDY.shp"
# Reading and converting to WGS84 CRS
polygon_data = gpd.read_file(polygon_shapefile).to_crs(epsg=4326)




st.header('RENEWABLE ENERGY INSTALLATIONS COUNT AND CAPACITY IN GOVERMENT BUILDINGS (STATE OWNED)')

# Streamlit app
#st.title('Jharkhand Map')
st.subheader('Hover over the districts for more information on Total Grid Connected Solar Rooftop Installations in Jharkhand')
st.header('ROOFTOP SOLAR')
# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor':'#10ef3b',
        'color': 'white',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.7,
    }
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, tiles='cartodb dark_matter',min_zoom =7,max_zoom=7)

folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['dtname','State_Solar_Capacity','State_Solar_Counts',], aliases=['District:','Grid Connected Rooftop Solar capacity:','Grid Connected Rooftop Solar count:'])

).add_to(m)
folium_static(m,width=600,height=400)

dfSRFY=pd.read_csv(r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\FY_GSR_insatllations.csv")
#Grid Connected Solar Rooftop Financial year wise counts in Jharkhand
dfSRFY_sorted = dfSRFY.sort_values(by='2022-23', ascending=True)
fig1 = px.bar(dfSRFY_sorted, y='Districts', x=['2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23'],
             title='Financial Year Wise Grid Connected Solar Rooftop Installations in Jharkhand',
             labels={'value': 'Installation Counts','variable': 'Financial Years'},
             template='plotly_dark',
             width=600, height=500)
fig1.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
fig1.update_yaxes(tickmode='array', tickvals=dfSRFY_sorted['Districts'], ticktext=dfSRFY_sorted['Districts'])
#fig1.show()
st.plotly_chart(fig1) 



dfGSRCAP=pd.read_csv(r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\FY_GSR_Capacity.csv")
#Grid Connected Solar Rooftop Capacity in Jharkhand
dfGSRCAP_sorted = dfGSRCAP.sort_values(by='2022-23', ascending=True)
fig2 = px.bar(dfSRFY_sorted, y='Districts', x=['2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23'],
             title='Financial Year Wise Installed Grid Connected Solar Rooftop Capacity in Jharkhand',
             labels={'value': 'Innstalled Capacity(kWp)','variable': 'Financial Years'},
             template='plotly_dark',
             width=600, height=500)
fig2.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
fig2.update_yaxes(tickmode='array', tickvals=dfSRFY_sorted['Districts'], ticktext=dfSRFY_sorted['Districts'])

#fig2.show()
st.plotly_chart(fig2) 




# Mini_Grid _solar_Count and Capacity Plots
st.header('MINI-GRID SOLAR')
# Read the CSV data
dfall = pd.read_csv(r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\All_Total.csv")
df4mgs=pd.read_csv(r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\Solar_Minigrid.csv")
# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'white',
        'weight':2,
        'dashArray': '4, 4',
        'fillOpacity': 0.7,
    }
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, tiles='cartodb dark_matter',min_zoom =7,max_zoom=7)
folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['dtname','State_SolarGrid_mini_plant','State_solarMinigrid_Plant_capacity'], aliases=['District:','Solar Minigrids count:','Solar Minigrids capacity:'])
).add_to(m)
folium.LayerControl().add_to(m)
folium_static(m,width=600,height=400)


df_sorted1 =df4mgs.sort_values(by='Minigrid_Capacity(kWp)',ascending=True)
fig3 = px.bar(df_sorted1, 
              y='Districts', 
              x='Minigrid_Capacity(kWp)', 
              text='Minigrid_Capacity(kWp)',  # Add this line for values in bar labels
              barmode='group', 
              title='Installed Minigrid Capacity(kWp)',
              labels={'Minigrid_Capacity(kWp)': 'Capacity (kWp)'},
              template='plotly_dark',
              width=600, height=500)

fig3.update_xaxes(title_text='Capacity (kWp)')
fig3.update_traces(texttemplate='%{text:.2s}(kWp)', textposition='inside')  # Adjust text formatting and position
fig3.update_yaxes(showticklabels=True, showgrid=True, zeroline=True)
st.plotly_chart(fig3)


st.header('SOLAR STREET LIGHTS ')

def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'white',
        'weight':2,
        'dashArray': '4, 4',
        'fillOpacity': 0.7,
    }
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, tiles='cartodb dark_matter',min_zoom =7,max_zoom=71)
folium.GeoJson(
    geojson_data,
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['dtname','Solar_streetlights_Count'], aliases=['District:','Solar Street lights Count:'])
).add_to(m)
folium.LayerControl().add_to(m)
folium_static(m,width=600,height=400)

fig5 = px.bar(dfST, x='Total', y='Dist',color='Total', barmode='group', title='Solar Streetlight installations')
fig5.update_yaxes(showticklabels=True, showgrid=True, zeroline=True,title_text='')
fig5.update_xaxes(showticklabels=True,showgrid=False,zeroline=True,title_text="Total installed Streetlights")
fig5.update_layout(
    yaxis=dict(
        tickmode='linear',
        dtick=1
    )
)
st.plotly_chart(fig5) 

st.title('Solar Rooftop Locations in the State of Jharkhand')
st.subheader('Goverment Hospitals installed solar panels')
# Load GeoJSON file
geojson_file = r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\Hospitals.geojson"
gdf = gpd.read_file(geojson_file)

# Ensure the 'Category' column is treated as categorical
gdf['Category'] = gdf['Category'].astype('str')

# Create a Folium map centered at the mean of the coordinates
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7,min_zoom=7, max_zoom=8, tiles='cartodb dark_matter', control_scale=True)

# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.4,
    }
# Define a custom icon with color (e.g., red)
#icon = folium.CustomIcon(icon_image=r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\icon.png", icon_size=(30, 30), icon_anchor=(15, 15), popup_anchor=(0, -15))
#icon = folium.Icon(color='red')
# Iterate through GeoDataFrame rows and add markers
for idx, row in gdf.iterrows():
    popup_text = row['Location']
    
    # Customize the icon size (adjust the icon_size parameter)
    icon_size = (2,2)  # Change the size according to your preference
    icon = folium.CustomIcon(icon_image=r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\icon.png", icon_size=(30, 30), icon_anchor=(15, 15), popup_anchor=(0, -15))
    folium.Marker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        popup=folium.Popup(popup_text, parse_html=True),
        icon=folium.Icon(color= 'yellow',icon='star',prefix='fa',icon_color='white')
    ).add_to(m)

# Add GeoJSON layer
folium.GeoJson(
    polygon_data,
    name='Jharkhand Districts',
).add_to(m)
folium.LayerControl().add_to(m)

# Display the Folium map using folium_static
folium_static(m, width=700, height=500)



st.subheader('Goverment Educational Institutions installed solar panels')

# Load GeoJSON file
geojson_file = r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\Educational_Instutions.geojson"
gdf = gpd.read_file(geojson_file)
# Ensure the 'Category' column is treated as categorical
gdf['Category'] = gdf['Category'].astype('str')

# Create a Folium map centered at the mean of the coordinates
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, min_zoom=7, max_zoom=8, tiles='cartodb dark_matter', control_scale=False)

# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.4,
    }

# Iterate through GeoDataFrame rows and add markers
for idx, row in gdf.iterrows():
    popup_text = row['Location']
    
    # Customize the icon size (adjust the icon_size parameter)
    icon_size = (2,2)  # Change the size according to your preference
    folium.Marker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        popup=folium.Popup(popup_text, parse_html=True),
        icon=folium.Icon(color= 'black',icon='star',prefix='fa',icon_color='white')
    ).add_to(m)

# Add GeoJSON layer
folium.GeoJson(
    polygon_data,
    name='Jharkhand Districts',
).add_to(m)
folium.LayerControl().add_to(m)
# Display the Folium map using folium_static
folium_static(m, width=700, height=500)



st.subheader('Goverment Miscellaneous Buildings installed solar panels')
# Load GeoJSON file
geojson_file = r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\Miscellaneous.geojson"
gdf = gpd.read_file(geojson_file)

# Ensure the 'Category' column is treated as categorical
gdf['Category'] = gdf['Category'].astype('str')

# Create a Folium map centered at the mean of the coordinates
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, min_zoom=7, max_zoom=8, tiles='cartodb dark_matter', control_scale=True)

# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.4,
    }

# Iterate through GeoDataFrame rows and add markers
for idx, row in gdf.iterrows():
    popup_text = row['Location']
    
    # Customize the icon size (adjust the icon_size parameter)
    icon_size = (2,2)  # Change the size according to your preference
    folium.Marker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        popup=folium.Popup(popup_text, parse_html=True),
        icon=folium.Icon(color= 'green',icon='star',prefix='fa',icon_color='white')
    ).add_to(m)

# Add GeoJSON layer
folium.GeoJson(
    polygon_data,
    name='Jharkhand Districts',
).add_to(m)
folium.LayerControl().add_to(m)
# Display the Folium map using folium_static
folium_static(m, width=700, height=500)



st.subheader('Goverment Buildings installed solar panels')
# Load GeoJSON file
geojson_file = r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\Govt_buildings.geojson"
gdf = gpd.read_file(geojson_file)

# Ensure the 'Category' column is treated as categorical
gdf['Category'] = gdf['Category'].astype('str')

# Create a Folium map centered at the mean of the coordinates
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, min_zoom=7, max_zoom=8, tiles='cartodb dark_matter', control_scale=True)

# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.4,
    }

# Add GeoJSON layer
folium.GeoJson(
    polygon_data,
    name='Jharkhand Districts',
).add_to(m)
# Iterate through GeoDataFrame rows and add markers
for idx, row in gdf.iterrows():
    popup_text = row['Location']
    
    # Customize the icon size (adjust the icon_size parameter)
    #icon=r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\police logo.png"
    icon_size = ()  # Change the size according to your preference
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=folium.Popup(popup_text, parse_html=True),
        icon=folium.Icon(color='pink',icon='star',prefix='fa',icon_color='white'),
    ).add_to(m)
    

folium.LayerControl().add_to(m)
# Display the Folium map using folium_static
folium_static(m, width=700, height=500)


st.subheader('Police Station installed solar panels')

geojson_file =r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\Police stations.geojson"
gdf = gpd.read_file(geojson_file)

# Ensure the 'Category' column is treated as categorical
gdf['Category'] = gdf['Category'].astype('str')

# Create a Folium map centered at the mean of the coordinates
m = folium.Map(location=[23.6345, 85.3803], zoom_start=7, min_zoom=7, max_zoom=8, tiles='cartodb dark_matter', control_scale=True)

# Function to customize tooltip
def style_function(feature):
    return {
        'fillColor': '#10ef3b',
        'color': 'Black',
        'weight': 2,
        'dashArray': '4, 4',
        'fillOpacity': 0.4,
    }

# Add GeoJSON layer
folium.GeoJson(
    polygon_data,
    name='Jharkhand Districts',
).add_to(m)

# Iterate through GeoDataFrame rows and add markers
for idx, row in gdf.iterrows():
    popup_text = row['Location']
    
    # Customize the icon size (adjust the icon_size parameter)
    #icon=r"C:\Users\sachi\OneDrive\Desktop\WEBAPPP\data\UPdated from JREDA\police logo.png"
    icon_size = ()  # Change the size according to your preference
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=folium.Popup(popup_text, parse_html=True),
        icon=folium.Icon(color= 'blue',icon='star',prefix='fa',icon_color='white'),
    ).add_to(m)
folium.LayerControl().add_to(m)
# Display the Folium map using folium_static
folium_static(m, width=700, height=500)




#st.header('Utlity grade (Ground Mounted) = PROJECT ONGOING')
st.header('Utility grade (Floating Solar) = PROJECT ONGOING' )
st.header('Utility grade (Canal Top Solar) =  WORK UNDER PROGRESS')












