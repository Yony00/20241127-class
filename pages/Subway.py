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
geojson_url = "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/SB10.geojson"

# 使用 requests 下載 GeoJSON 檔案
response = requests.get(geojson_url)

import requests
import geopandas as gpd

# 替換為您的 GeoJSON 文件的 URL
url = "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/SB10.geojson"

# 發送請求
response = requests.get(url)

if response.status_code == 200:
    print("Successfully downloaded GeoJSON file!")
    
    # 將文件內容讀取為 GeoPandas 資料框
    gdf = gpd.read_file(response.text)
    
    # 打印 GeoDataFrame 的頭幾行數據
    print(gdf.head())
else:
    print(f"Failed to download GeoJSON file. Status code: {response.status_code}")
