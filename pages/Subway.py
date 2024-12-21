
import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import requests
from shapely.geometry import Point

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
    
    # 計算最近的速食餐廳
    geojson_url = "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/output.geojson"

    # 使用 requests 下載 GeoJSON 檔案
    response = requests.get(geojson_url)

    if response.status_code == 200:
        # 將下載的資料轉換為 GeoJSON 格式
        gdf = gpd.read_file(response.text)

        # 顯示 GeoDataFrame 欄位，確保使用正確的欄位名稱
        st.write("Columns in GeoDataFrame:", gdf.columns)  # 顯示欄位

        # 將點擊的座標轉換為 Point 物件
        clicked_point_geom = Point(lon, lat)

        # 計算每個速食餐廳到點擊位置的距離
        gdf['distance'] = gdf.geometry.distance(clicked_point_geom)

        # 找到最近的餐廳
        nearest_restaurant = gdf.loc[gdf['distance'].idxmin()]

        # 檢查最近餐廳是否包含經緯度
        if 'geometry' in nearest_restaurant:
            nearest_lat = nearest_restaurant.geometry.y
            nearest_lon = nearest_restaurant.geometry.x
            st.write(f"Nearest Fast Food Restaurant:")
            st.write(f"Name: {nearest_restaurant['name']}")
            st.write(f"Latitude: {nearest_lat}")
            st.write(f"Longitude: {nearest_lon}")
            st.write(f"Distance: {nearest_restaurant['distance']:.2f} meters")
        else:
            st.error("The nearest restaurant's location data is missing.")
    else:
        st.error("Failed to download GeoJSON file from GitHub.")
else:
    st.info("Click on the map to get the coordinates.")
