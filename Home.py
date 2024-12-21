import streamlit as st
import folium
import geopandas as gpd
import requests
import pandas as pd  # 加入 pandas 模組
from streamlit_folium import st_folium

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

    # 檢查合併後的欄位名稱
    st.write("Columns in Combined GeoDataFrame:", combined_gdf.columns)

    # 初始化地圖，將地圖中心設置為第一個速食餐廳的位置
    first_location = combined_gdf.geometry.iloc[0].coords[0]
    m = folium.Map(location=[first_location[1], first_location[0]], zoom_start=12)

    # 自定義每個來源的圖標
    icons = [
        "https://cdn-icons-png.flaticon.com/512/1046/1046784.png",  # 第一個來源的圖標
        "https://cdn-icons-png.flaticon.com/512/1046/1046846.png",  # 第二個來源的圖標
        "https://cdn-icons-png.flaticon.com/512/1046/1046825.png"   # 第三個來源的圖標
    ]

    # 根據不同來源選擇圖標
    for idx, row in combined_gdf.iterrows():
        lat, lon = row.geometry.y, row.geometry.x
        source_index = row.get("source_index", idx % len(geojson_urls))  # 用來區分資料來源
        icon_url = icons[source_index % len(icons)]  # 根據來源選擇圖標
        custom_icon = folium.CustomIcon(icon_url, icon_size=(30, 30))

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
    st_folium(m, width=700)

    # 顯示合併後的餐廳列表
    if 'name' in combined_gdf.columns:
        st.write("Combined Restaurant Locations:")
        st.write(combined_gdf[['name', 'number', 'address','hours']])
    else:
        st.write("Column 'name' not found in the combined GeoJSON data.")
else:
    st.error("No valid GeoJSON data could be loaded.")
