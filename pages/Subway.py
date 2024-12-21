import streamlit as st
import folium
import geopandas as gpd
import requests
from streamlit_folium import st_folium

# 設定頁面標題
st.title("Fast Food Restaurants Map with Custom Markers")

# 下載 GitHub 上的 GeoJSON 檔案
geojson_url = "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/output.geojson"

# 使用 requests 下載 GeoJSON 檔案
response = requests.get(geojson_url)

if response.status_code == 200:
    # 將下載的資料轉換為 GeoJSON 格式
    gdf = gpd.read_file(response.text)

    # 檢查 GeoDataFrame 中的欄位名稱
    st.write("Columns in GeoDataFrame:", gdf.columns)

    # 初始化地圖，將地圖中心設置為第一個餐廳的位置
    first_location = gdf.geometry.iloc[0].coords[0]
    m = folium.Map(location=[first_location[1], first_location[0]], zoom_start=12)

    # 將餐廳位置加入地圖，使用自定義圖標
    for idx, row in gdf.iterrows():
        lat, lon = row.geometry.y, row.geometry.x
        # 使用自定義圖標
        icon_url = "https://cdn-icons-png.flaticon.com/512/1046/1046784.png"  # 替換為您想使用的圖標 URL
        custom_icon = folium.CustomIcon(icon_url, icon_size=(30, 30))  # 設定圖標大小
        folium.Marker(
            location=[lat, lon],
            popup=f"{row['name']}",  # 替換為您的資料欄位
            icon=custom_icon
        ).add_to(m)

    # 顯示地圖
    st_folium(m, width=700)

    # 顯示餐廳列表（根據實際欄位名稱）
    if 'name' in gdf.columns and 'address' in gdf.columns:
        st.write("Restaurant Locations:")
        st.write(gdf[['name', 'address']])
    else:
        st.write("Columns 'name' and 'address' not found in the GeoJSON data.")
else:
    st.error("Failed to download GeoJSON file from GitHub.")
