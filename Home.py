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
geojson_urls = [
    "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/SB10.geojson",  # 第一間速食餐廳
    "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/KK10.geojson",  # 第二間速食餐廳
    "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/MM10.geojson"   # 第三間速食餐廳
]

geo_dfs = []

# 下載和讀取每個 GeoJSON 檔案
for url in geojson_urls:
    response = requests.get(url)
    if response.status_code == 200:
        geo_dfs.append(gpd.read_file(response.text))
    else:
        st.error(f"Failed to download GeoJSON file from: {url}")

# 合併所有 GeoDataFrame
if geo_dfs:
    combined_gdf = gpd.GeoDataFrame(pd.concat(geo_dfs, ignore_index=True))  # 使用 pd.concat 合併 GeoDataFrame

    # 顯示速食餐廳選單
    restaurant_names = combined_gdf['name'].unique()
    selected_restaurant = st.selectbox("選擇一間速食餐廳", restaurant_names)

    # 根據選擇的速食餐廳過濾資料
    selected_data = combined_gdf[combined_gdf['name'] == selected_restaurant]

    # 初始化地圖，將地圖中心設置為選擇餐廳的位置
    lat, lon = selected_data.geometry.y.iloc[0], selected_data.geometry.x.iloc[0]
    m = folium.Map(location=[lat, lon], zoom_start=15)

    # 自定義圖標
    icon_url = "https://cdn-icons-png.flaticon.com/512/3027/3027137.png"  # 使用薯條的圖標
    custom_icon = folium.CustomIcon(icon_url, icon_size=(30, 30))

    # 使用 HTML 格式來顯示 popup 內容
    row = selected_data.iloc[0]
    popup_content = f"""
    <strong>分店:</strong> {row['name'] if 'name' in row else 'Unknown'}<br>
    <strong>電話:</strong> {row['number'] if 'number' in row else 'Not Available'}<br>
    <strong>地址:</strong> {row['address'] if 'address' in row else 'Not Available'}<br>
    <strong>營業時間:</strong> {row['hours'] if 'hours' in row else 'Not Available'}<br>
    """

    # 在地圖上添加選擇的速食餐廳標記
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_content, max_width=300),  # 使用自定義的 popup 內容
        icon=custom_icon
    ).add_to(m)

    # 顯示選擇的速食餐廳資訊
    st.write("選擇的速食餐廳資訊:")
    st.write(f"名稱: {row['name']}")
    st.write(f"電話: {row['number'] if 'number' in row else 'Not Available'}")
    st.write(f"地址: {row['address'] if 'address' in row else 'Not Available'}")
    st.write(f"營業時間: {row['hours'] if 'hours' in row else 'Not Available'}")

    # 顯示放大後的地圖
    st_folium(m, width=1000, height=800)  # 增加 height 來放大地圖
else:
    st.error("No valid GeoJSON data could be loaded.")
