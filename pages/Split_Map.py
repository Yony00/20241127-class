import streamlit as st
from streamlit_folium import st_folium
import folium

st.title("Interactive Map - Click to Get Coordinates")

# 初始化地圖
m = folium.Map(location=[0, 0], zoom_start=2)

# 添加地圖點擊處理
def map_click_callback(map_object, lat, lon):
    folium.Marker(location=[lat, lon], tooltip=f"Lat: {lat}, Lon: {lon}").add_to(map_object)

# Streamlit 的 Folium 擴展可以處理互動
clicked_point = st_folium(m, key="folium_map")

# 提取點擊座標
if clicked_point and clicked_point["last_clicked"]:
    lat = clicked_point["last_clicked"]["lat"]
    lon = clicked_point["last_clicked"]["lng"]
    st.success(f"You clicked at Latitude: {lat}, Longitude: {lon}")
