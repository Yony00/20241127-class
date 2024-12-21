import streamlit as st
import folium
import geopandas as gpd
import requests
import pandas as pd  # 加入 pandas 模組
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# 設定頁面標題
st.title("發現鄰近美味！速食餐廳互動式地圖")

# 定義 GeoJSON 檔案的 URL
geojson_urls = {
    "麥當勞": "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/SB10.geojson",
    "肯德基": "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/KK10.geojson",
    "Subway": "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/MM10.geojson"
}

geo_dfs = {}

# 下載和讀取每個 GeoJSON 檔案
for restaurant, url in geojson_urls.items():
    response = requests.get(url)
    if response.status_code == 200:
        geo_dfs[restaurant] = gpd.read_file(response.text)
    else:
        st.error(f"Failed to download GeoJSON file from: {url}")

# 顯示選單，讓用戶選擇顯示哪一間速食餐廳
restaurant_choice = st.selectbox(
    "選擇您想查看的速食餐廳：", list(geojson_urls.keys())
)

# 顯示選擇的速食餐廳的地圖
if restaurant_choice in geo_dfs:
    selected_gdf = geo_dfs[restaurant_choice]

    # 初始化地圖，將地圖中心設置為指定的座標
    m = folium.Map(location=[23.6, 121], zoom_start=8)  # 地圖尺度設置為 (23.6, 121)

    # 自定義圖標 URL
    icons = {
        "麥當勞": "https://cdn-icons-png.flaticon.com/512/1046/1046784.png",
        "肯德基": "https://cdn-icons-png.flaticon.com/512/1046/1046846.png",
        "Subway": "https://cdn-icons-png.flaticon.com/512/1046/1046825.png"
    }

    # 根據選擇的餐廳設置圖標
    icon_url = icons[restaurant_choice]
    custom_icon = folium.CustomIcon(icon_url, icon_size=(30, 30))

    # 顯示選擇餐廳的詳細資料
    for idx, row in selected_gdf.iterrows():
        lat, lon = row.geometry.y, row.geometry.x

        # 使用 HTML 格式來顯示 popup 內容
        popup_content = f"""
        <strong>分店:</strong> {row['name'] if 'name' in row else 'Unknown'}<br>
        <strong>電話:</strong> {row['number'] if 'number' in row else 'Not Available'}<br>
        <strong>地址:</strong> {row['address'] if 'address' in row else 'Not Available'}<br>
        <strong>營業時間:</strong> {row['hours'] if 'hours' in row else 'Not Available'}<br>
        """

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_content, max_width=300),  # 使用自定義的 popup 內容
            icon=custom_icon
        ).add_to(m)

    # 顯示地圖
    st_folium(m, width=900, height=600)

    # 顯示餐廳的基本資料表
    st.write(f"{restaurant_choice} 餐廳位置列表:")
    st.write(selected_gdf[['name', 'number', 'address', 'hours']])
else:
    st.error("No valid GeoJSON data could be loaded.")
