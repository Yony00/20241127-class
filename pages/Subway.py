import streamlit as st
import folium
from streamlit_folium import st_folium
import json

# 標題
st.title("Fast Food Restaurants JSON Upload and Display on Map")

# 上傳 JSON 檔案
uploaded_file = st.file_uploader("https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/output.geojson", type=["geojson"])

if uploaded_file is not None:
    # 讀取並解析 JSON 檔案
    file_content = uploaded_file.getvalue().decode("utf-8")
    
    try:
        data = json.loads(file_content)
        restaurants = data.get("restaurants", [])
        
        # 初始化地圖
        m = folium.Map(location=[20, 0], zoom_start=2)  # 設定地圖中心與縮放
        
        for restaurant in restaurants:
            name = restaurant.get("name", "Unknown Restaurant")
            lat = restaurant.get("lat")
            lon = restaurant.get("lon")
            
            if lat is not None and lon is not None:
                # 在地圖上添加標記
                folium.Marker([lat, lon], popup=name).add_to(m)
        
        # 顯示地圖
        st_folium(m, width=700, height=500)
        
    except Exception as e:
        st.error(f"Error parsing JSON file: {e}")
