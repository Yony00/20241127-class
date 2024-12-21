import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import requests

st.title("Interactive Map - Click to Get Coordinates")

# 初始化地圖
m = folium.Map(location=[23.6, 121], zoom_start=8)

# 在地圖上點擊時，會更新並顯示座標
clicked_point = st_folium(m, key="folium_map")

# 提取點擊座標
if clicked_point and clicked_point.get("last_clicked"):
    lat = clicked_point["last_clicked"]["lat"]
    lon = clicked_point["last_clicked"]["lng"]
    st.success(f"You clicked at Latitude: {lat}, Longitude: {lon}")
else:
    st.info("Click on the map to get the coordinates.")
    
# 設定頁面標題
st.title("Fast Food Restaurants Map")

# 下載 GitHub 上的 GeoJSON 檔案
geojson_url = "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/output.geojson"

# 使用 requests 下載 GeoJSON 檔案
response = requests.get(geojson_url)

if response.status_code == 200:
    # 將下載的資料轉換為 GeoJSON 格式
    gdf = gpd.read_file(response.text)

    # 初始化地圖，將地圖中心設置為第一個餐廳的位置
    first_location = gdf.geometry.iloc[0].coords[0]
    m = folium.Map(location=[first_location[1], first_location[0]], zoom_start=12)

    # 將 GeoJSON 資料加到地圖上
    folium.GeoJson(gdf).add_to(m)

    # 顯示地圖
    st_folium(m, width=700)

    # 顯示餐廳列表
    st.write("Restaurant Locations:")
    st.write(gdf[['name', 'address']])
else:
    st.error("Failed to download GeoJSON file from GitHub.")
