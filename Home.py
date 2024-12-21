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
    "麥當勞": "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/SB10.geojson",  # 麥當勞
    "肯德基": "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/KK10.geojson",  # 肯德基
    "Subway": "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/MM10.geojson"   # Subway
}

geo_dfs = []

# 讓使用者選擇速食餐廳
restaurant_choice = st.selectbox("選擇速食餐廳", list(geojson_urls.keys()))

# 下載和讀取選擇的速食餐廳 GeoJSON 檔案
selected_url = geojson_urls[restaurant_choice]
response = requests.get(selected_url)
if response.status_code == 200:
    geo_dfs.append(gpd.read_file(response.text))
else:
    st.error(f"Failed to download GeoJSON file from: {selected_url}")

# 合併所有 GeoDataFrame
if geo_dfs:
    combined_gdf = gpd.GeoDataFrame(pd.concat(geo_dfs, ignore_index=True))  # 使用 pd.concat 合併 GeoDataFrame

    # 初始化地圖，將地圖中心設置為指定的座標
    m = folium.Map(location=[23.6, 121], zoom_start=8)  # 地圖尺度設置為 (23.6, 121)

    # 自定義圖標
    icon_url = "https://cdn-icons-png.flaticon.com/512/3027/3027137.png"  # 薯條圖標
    custom_icon = folium.CustomIcon(icon_url, icon_size=(30, 30))

    # 顯示餐廳的分店位置
    for idx, row in combined_gdf.iterrows():
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

    # 顯示放大後的地圖
    st_folium(m, width=1000, height=800)  # 增加 height 來放大地圖

    # 顯示餐廳列表
    if 'name' in combined_gdf.columns:
        st.write(f"{restaurant_choice} 分店位置:")
        st.write(combined_gdf[['name', 'number', 'address', 'hours']])
else:
    st.error("No valid GeoJSON data could be loaded.")
