# main.py
import streamlit as st
import leafmap.foliumap as leafmap
from forest_health import get_ndvi
import tempfile

st.set_page_config(layout="wide")
st.title("🌳 Open Forest Monitor")

# Sidebar navigation
option = st.sidebar.radio("Choose Monitoring Mode:", ["Forest Health", "Degradation", "Deforestation", "Fire"])

if option == "Forest Health":
    st.subheader("🟢 Forest Health Viewer (NDVI)")
    lat_center = -4.05
    lon_center = 39.67
    bbox = [39.6, -4.2, 39.8, -3.9]

    st.markdown("**Monitoring region:** Mombasa County")
    if st.button("Compute NDVI"):
        ndvi = get_ndvi(bbox)
        with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as tmp:
            ndvi.rio.to_raster(tmp.name)
            m = leafmap.Map(center=(lat_center, lon_center), zoom=11)
            m.add_raster(tmp.name, layer_name="NDVI", colormap="Greens", nodata=0)
            m.to_streamlit(height=500)
