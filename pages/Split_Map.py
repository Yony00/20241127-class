import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Split-panel Map")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map()
        m.split_map(
            left_layer="https://github.com/Yony00/tiff-to-http2/raw/refs/heads/main/image%20(1).tif", right_layer="https://github.com/Yony00/tiff-to-http2/raw/refs/heads/main/tree.tif"
        )
        m.add_legend(title="https://github.com/Yony00/tiff-to-http2/raw/refs/heads/main/image%20(1).tif", builtin_legend="https://github.com/Yony00/tiff-to-http2/raw/refs/heads/main/tree.tif")

m.to_streamlit(height=700)
