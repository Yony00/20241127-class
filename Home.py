import streamlit as st
import folium
import geopandas as gpd
import requests
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# 設定頁面標題
st.title("速食餐廳地圖展示")

# 定義速食餐廳 GeoJSON 檔案的 URL
geojson_urls = {
    "Subway": "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/SB10.geojson",
    "肯德基": "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/KK10.geojson",
    "麥當勞": "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/MM10.geojson"
}

# 下載 GeoJSON 資料
geo_dfs = []
for name, url in geojson_urls.items():
    response = requests.get(url)
    if response.status_code == 200:
        geo_dfs.append((name, gpd.read_file(response.text)))
    else:
        st.error(f"Failed to download GeoJSON file from: {url}")

# 顯示速食餐廳選單
restaurant_choice = st.selectbox("選擇速食餐廳", ["麥當勞", "肯德基", "Subway"])

# 根據選擇過濾對應的 GeoDataFrame
selected_gdf = next(gdf for name, gdf in geo_dfs if name == restaurant_choice)

# 顯示選擇的餐廳列表
if 'name' in selected_gdf.columns:
    st.write(f"{restaurant_choice} 的餐廳位置:")
    st.write(selected_gdf[['name', 'number', 'address', 'hours']])

    # 初始化地圖，設置地圖的中心位置
    m = folium.Map(location=[23.6, 121], zoom_start=8)

    # 自定義圖標 URL
    icons = {
        "麥當勞": "https://cdn-icons-png.flaticon.com/512/1046/1046784.png",
        "肯德基": "https://cdn-icons-png.flaticon.com/512/1046/1046846.png",
        "Subway": "https://cdn-icons-png.flaticon.com/512/1046/1046825.png"
    }

    # 根據選擇的餐廳選擇圖標
    icon_url = icons[restaurant_choice]
    custom_icon = folium.CustomIcon(icon_url, icon_size=(30, 30))

    # 顯示地圖上的標記
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
            popup=folium.Popup(popup_content, max_width=300),
            icon=custom_icon
        ).add_to(m)

    # 顯示放大後的地圖
    st_folium(m, width=900, height=600)

else:
    st.write("No restaurant data available.")

# 下面是展示所有三個餐廳分開地圖的部分

st.write("### 麥當勞 地圖展示")
m_mcdonalds = folium.Map(location=[23.6, 121], zoom_start=8)
for idx, row in geo_dfs[0][1].iterrows():
    lat, lon = row.geometry.y, row.geometry.x
    folium.Marker(
        location=[lat, lon],
        popup=row['name'],
        icon=folium.CustomIcon("https://cdn-icons-png.flaticon.com/512/1046/1046784.png", icon_size=(30, 30))
    ).add_to(m_mcdonalds)
st_folium(m_mcdonalds, width=900, height=600)

st.write("### 肯德基 地圖展示")
m_kfc = folium.Map(location=[23.6, 121], zoom_start=8)
for idx, row in geo_dfs[1][1].iterrows():
    lat, lon = row.geometry.y, row.geometry.x
    folium.Marker(
        location=[lat, lon],
        popup=row['name'],
        icon=folium.CustomIcon("https://cdn-icons-png.flaticon.com/512/1046/1046846.png", icon_size=(30, 30))
    ).add_to(m_kfc)
st_folium(m_kfc, width=900, height=600)

st.write("### Subway 地圖展示")
m_subway = folium.Map(location=[23.6, 121], zoom_start=8)
for idx, row in geo_dfs[2][1].iterrows():
    lat, lon = row.geometry.y, row.geometry.x
    folium.Marker(
        location=[lat, lon],
        popup=row['name'],
        icon=folium.CustomIcon("https://cdn-icons-png.flaticon.com/512/1046/1046825.png", icon_size=(30, 30))
    ).add_to(m_subway)
st_folium(m_subway, width=900, height=600)
