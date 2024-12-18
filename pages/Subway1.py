import streamlit as st
import folium
import geopandas as gpd
import requests
from shapely.geometry import Point
from streamlit_folium import st_folium

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

    # 顯示所有餐廳點位
    for idx, row in gdf.iterrows():
        folium.Marker([row.geometry.y, row.geometry.x], popup=row['name']).add_to(m)

    # 顯示地圖
    st_folium(m, width=700)

    # 提取點擊座標
    clicked_point = st_folium(m, key="folium_map")

    if clicked_point and clicked_point.get("last_clicked"):
        lat = clicked_point["last_clicked"]["lat"]
        lon = clicked_point["last_clicked"]["lng"]
        st.success(f"You clicked at Latitude: {lat}, Longitude: {lon}")

        # 將點擊的座標轉換為 Point 物件
        clicked_point_geom = Point(lon, lat)

        # 計算每個速食餐廳到點擊位置的距離
        gdf['distance'] = gdf.geometry.distance(clicked_point_geom)

        # 找到最近的餐廳
        nearest_restaurant = gdf.loc[gdf['distance'].idxmin()]

        # 顯示最近餐廳的資訊
        st.write(f"Nearest Fast Food Restaurant:")
        st.write(f"Name: {nearest_restaurant['name']}")
        st.write(f"Latitude: {nearest_restaurant.geometry.y}")
        st.write(f"Longitude: {nearest_restaurant.geometry.x}")
        st.write(f"Distance: {nearest_restaurant['distance']:.2f} meters")

        # 在地圖上標註最近餐廳
        folium.Marker(
            [nearest_restaurant.geometry.y, nearest_restaurant.geometry.x],
            popup=f"Nearest: {nearest_restaurant['name']}",
            icon=folium.Icon(color='green')
        ).add_to(m)

        # 顯示更新後的地圖
        st_folium(m, width=700)

else:
    st.error("Failed to download GeoJSON file from GitHub.")
