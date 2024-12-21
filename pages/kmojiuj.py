import streamlit as st
import pandas as pd
import numpy as np
import folium
import geopy.distance
import geopandas as gpd
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("餐廳搜尋 - 以地圖點選搜尋餐廳")

# 假設餐廳的 GeoJSON 檔案 URL
restaurant_url = "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/KK10.geojson"

# 讀取餐廳 GeoJSON 檔案
restaurants = gpd.read_file(restaurant_url)

# 初始化地圖
m = folium.Map(location=[23.15, 120.3], zoom_start=12)

# 設定標註群組
marker_cluster = MarkerCluster().add_to(m)

# 在地圖上標註所有餐廳
for _, row in restaurants.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=row['name'],  # 假設有餐廳名稱
    ).add_to(marker_cluster)

# 監聽地圖點選
clicked_location = st_folium(m, width=700, height=500)

# 如果有點選位置，則開始進行搜尋
if clicked_location:
    click_lat = clicked_location['lat']
    click_lon = clicked_location['lon']
    st.write(f"您選擇的位置：經度 {click_lon}, 緯度 {click_lat}")

    # 計算並顯示3公里範圍內的餐廳
    nearby_restaurants = []
    for _, row in restaurants.iterrows():
        restaurant_coords = (row['lat'], row['lon'])
        clicked_coords = (click_lat, click_lon)
        distance = geopy.distance.distance(restaurant_coords, clicked_coords).km
        if distance <= 3:
            nearby_restaurants.append(row)

    # 顯示範圍內的餐廳
    if nearby_restaurants:
        st.write(f"範圍內有 {len(nearby_restaurants)} 家餐廳：")
        for restaurant in nearby_restaurants:
            st.write(f"- {restaurant['name']}, 距離: {distance:.2f} 公里")

        # 在地圖上標註範圍內的餐廳
        for restaurant in nearby_restaurants:
            folium.Marker(
                location=[restaurant['lat'], restaurant['lon']],
                popup=restaurant['name'],
                icon=folium.Icon(color="green"),
            ).add_to(m)

        # 顯示更新後的地圖
        st_folium(m, width=700, height=500)
    else:
        st.write("範圍內沒有餐廳")
