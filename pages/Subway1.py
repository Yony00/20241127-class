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



import streamlit as st
import folium
import geopandas as gpd
import requests
from shapely.geometry import Point
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# 設定頁面標題
st.title("Fast Food Restaurants Map with Click and Nearest Location")

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

        # 顯示最近餐廳的圖
        fig, ax = plt.subplots(figsize=(8, 6))

        # 顯示餐廳的座標
        ax.scatter(gdf.geometry.x, gdf.geometry.y, c='blue', label='Restaurants', alpha=0.6)
        ax.scatter(lon, lat, c='red', label='Clicked Location', zorder=5)
        ax.scatter(nearest_restaurant.geometry.x, nearest_restaurant.geometry.y, c='green', label='Nearest Restaurant', zorder=5)

        # 標註餐廳和點擊位置
        ax.text(lon, lat, '  Clicked Location', fontsize=12, ha='right', color='red')
        ax.text(nearest_restaurant.geometry.x, nearest_restaurant.geometry.y, '  Nearest Restaurant', fontsize=12, ha='left', color='green')

        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title("Clicked Location and Nearest Restaurant")

        ax.legend()

        # 顯示圖形
        st.pyplot(fig)

else:
    st.error("Failed to download GeoJSON file from GitHub.")
