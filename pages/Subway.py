import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from shapely.geometry import Point
import geopandas as gpd

st.set_page_config(layout="wide")
st.title("地震災害防治分析—以美濃地震為例")

st.header("環境介紹")
st.subheader("📌歷史地震點位展示")
st.write("下方圖台為1973年1月至2024年9月為止規模5以上的地震震央點位及相關資料")
url = "https://raw.githubusercontent.com/liuchia515/gisappreport/refs/heads/main/data/%E6%AD%B7%E5%8F%B2%E8%B3%87%E6%96%99.csv"
data = pd.read_csv(url)

cola, colb = st.columns([2, 1])

# 篩選範圍調整
selected = st.slider("請依照需求自行調整範圍", 5.0, 7.3, (5.0, 7.3))

def filterdata(df, selected_range):
    lower, upper = selected_range
    return df[(df["ML"] >= lower) & (df["ML"] <= upper)]

filtered_data = filterdata(data, selected)

with cola:
    st.map(filtered_data, size=20, color="#0044ff")

# 環域生成函數
def create_buffer(lat, lon, radius_km=10, num_points=50):
    """生成一個圓形的多邊形範圍"""
    earth_radius_km = 6371.0
    points = []
    for angle in np.linspace(0, 360, num_points):
        angle_rad = np.radians(angle)
        dlat = radius_km / earth_radius_km * np.cos(angle_rad)
        dlon = radius_km / (earth_radius_km * np.cos(np.radians(lat))) * np.sin(angle_rad)
        points.append([lon + np.degrees(dlon), lat + np.degrees(dlat)])
    return points

# 添加互動式環域
if st.button("點擊顯示環域"):
    st.subheader("環域展示")
    buffer_list = []
    for _, row in filtered_data.iterrows():
        buffer = create_buffer(row["latitude"], row["longitude"], radius_km=10)
        buffer_list.append({"coordinates": [buffer], "id": row["ML"]})

    # 將多邊形範圍添加到 pydeck
    buffer_layer = pdk.Layer(
        "PolygonLayer",
        data=buffer_list,
        get_polygon="coordinates",
        get_fill_color=[0, 0, 255, 50],
        get_line_color=[0, 0, 255],
        line_width_min_pixels=2,
        pickable=True,
    )

    point_layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_data,
        get_position="[longitude, latitude]",
        get_radius=10000,  # 震央的半徑樣式
        get_fill_color=[255, 0, 0],
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=23.15,
        longitude=120.3,
        zoom=8,
        pitch=30,
    )

    r = pdk.Deck(
        layers=[buffer_layer, point_layer],
        initial_view_state=view_state,
        tooltip={"text": "震央規模: {id}"},
    )

    st.pydeck_chart(r)

with colb:
    st.write("選定規模範圍內地震資料")
    st.dataframe(filtered_data)
