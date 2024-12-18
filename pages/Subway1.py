import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import requests
from shapely.geometry import Point
from io import StringIO

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
        geojson_data = StringIO(response.text)
        gdf = gpd.read_file(geojson_data)

        # 將點擊的座標轉換為 Point 物件
        clicked_point_geom = Point(lon, lat)

        # 轉換到適合計算距離的坐標系（EPSG:4326），這是經緯度坐標系
        gdf = gdf.to_crs(epsg=4326)

        # 計算每個速食餐廳到點擊位置的距離
        gdf['distance'] = gdf.geometry.distance(clicked_point_geom)

        # 找到最近的餐廳
        nearest_restaurant = gdf.loc[gdf['distance'].idxmin()]

        # 顯示最近餐廳的資訊
        st.write(f"Nearest Fast Food Restaurant:")
        st.write(f"Name: {nearest_restaurant['name']}")
        st.write(f"Address: {nearest_restaurant['address']}")
        st.write(f"Distance: {nearest_restaurant['distance']:.2f} meters")
    else:
        st.error("Failed to download GeoJSON file from GitHub.")
    
    # 繪製所有速食餐廳的點位
    for _, restaurant in gdf.iterrows():
        folium.Marker(
            location=[restaurant.geometry.y, restaurant.geometry.x], 
            popup=f"{restaurant['name']}<br>{restaurant['address']}", 
            icon=folium.Icon(color='blue')
        ).add_to(m)

    # 繪製最近的餐廳標記
    folium.Marker(
        location=[nearest_restaurant.geometry.y, nearest_restaurant.geometry.x], 
        popup=f"Nearest: {nearest_restaurant['name']}<br>{nearest_restaurant['address']}",
        icon=folium.Icon(color='red')
    ).add_to(m)
else:
    st.info("Click on the map to get the coordinates.")

# 顯示地圖
st_folium(m, width=700)
