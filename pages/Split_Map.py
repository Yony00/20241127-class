import streamlit as st
import pydeck as pdk
import pandas as pd

# 預設地圖中心
default_lat, default_lon = 0, 0

st.title("Interactive Map Click Coordinates")

# 初始化數據框，用於存儲點擊的座標
if "clicked_points" not in st.session_state:
    st.session_state["clicked_points"] = []

# 點擊事件處理
def add_point(lat, lon):
    st.session_state["clicked_points"].append({"lat": lat, "lon": lon})

# 地圖展示
st.subheader("Click on the map to get coordinates")
map_data = pd.DataFrame(st.session_state["clicked_points"])

# pydeck 配置
view_state = pdk.ViewState(
    latitude=default_lat, longitude=default_lon, zoom=2, pitch=0
)
layers = [
    pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position="[lon, lat]",
        get_color="[200, 30, 0, 160]",
        get_radius=100000,
    )
]

# 顯示地圖
st.pydeck_chart(
    pdk.Deck(
        initial_view_state=view_state,
        layers=layers,
        map_style="mapbox://styles/mapbox/streets-v11",
        tooltip={"html": "<b>Lat:</b> {lat}<br><b>Lon:</b> {lon}"},
    )
)

# 模擬地圖點擊事件 (手動輸入座標)
st.sidebar.header("Add Coordinates")
lat = st.sidebar.number_input("Latitude", min_value=-90.0, max_value=90.0, step=0.01)
lon = st.sidebar.number_input("Longitude", min_value=-180.0, max_value=180.0, step=0.01)
if st.sidebar.button("Add Point"):
    add_point(lat, lon)

# 展示所有點擊的座標
st.subheader("Clicked Points")
st.write(map_data)
