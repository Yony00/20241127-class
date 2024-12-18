from ipyleaflet import Map, Marker, basemaps
import ipywidgets as widgets
from ipywidgets import VBox, HTML
from IPython.display import display, clear_output

# 設置上方地圖
top_map = Map(center=(0, 0), zoom=2, basemap=basemaps.OpenStreetMap.Mapnik, scroll_wheel_zoom=True, layout={'height': '500px', 'width': '100%'})

# 設置下方地圖
output = widgets.Output()
with output:
    bottom_map = Map(center=(0, 0), zoom=2, basemap=basemaps.Esri.WorldImagery, scroll_wheel_zoom=True, layout={'height': '500px', 'width': '100%'})
    display(bottom_map)

# 定義計算對蹠點的函數
def calculate_antipode(lat, lon):
    antipode_lat = -lat
    antipode_lon = lon + 180 if lon < 0 else lon - 180
    return antipode_lat, antipode_lon

# 提示點選位置和對蹠點的經緯度
coords_label = HTML(value="<span style='font-size: 24px;'><b>點選位置:</b> ( , ) | <b>對蹠點:</b> ( , )</span>", layout={'margin': '10px 0px'})

# 初始化上方地圖的標記變量
top_marker = None

# 定義點擊事件處理函數
def handle_map_click(**kwargs):
    global top_marker
    if kwargs.get('type') == 'click':
        lat, lon = kwargs['coordinates']  # 獲取點擊位置的經緯度
        antipode_lat, antipode_lon = calculate_antipode(lat, lon)

        # 更新顯示經緯度的標籤，並設置字體大小為 24px
        coords_label.value = f"<span style='font-size: 24px;'><b>點選位置:</b> ({lat:.6f}, {lon:.6f}) | <b>對蹠點:</b> ({antipode_lat:.6f}, {antipode_lon:.6f})</span>"

        # 移除舊的標記並在上方地圖上標記新點
        if top_marker:
            top_map.remove_layer(top_marker)
        top_marker = Marker(location=(lat, lon), draggable=False)
        top_map.add_layer(top_marker)

        # 更新下方地圖
        update_bottom_map(antipode_lat, antipode_lon)

def update_bottom_map(lat, lon):
    global bottom_map, output

    # 移除舊的地圖顯示
    output.clear_output()

    # 創建新的 bottom_map，並設置為衛星影像圖
    bottom_map = Map(center=(lat, lon), zoom=5, basemap=basemaps.Esri.WorldImagery, scroll_wheel_zoom=True, layout={'height': '400px', 'width': '100%'})

    # 添加新的對蹠點標記
    bottom_marker = Marker(location=(lat, lon), draggable=False)
    bottom_map.add_layer(bottom_marker)

    # 顯示新的 bottom_map
    with output:
        display(bottom_map)

# 添加點擊事件到上方地圖
top_map.on_interaction(handle_map_click)

# 顯示上下兩個地圖及經緯度標籤
display(VBox([top_map, output, coords_label]))
