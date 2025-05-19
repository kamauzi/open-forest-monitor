# main.py

import streamlit as st
import leafmap.foliumap as leafmap
from forest_health import get_ndvi
import tempfile
import gc

st.set_page_config(layout="wide")
st.title("🌳 Open Forest Monitor")

# Sidebar navigation
option = st.sidebar.radio("Choose Monitoring Mode:", ["Forest Health", "Degradation", "Deforestation", "Fire"])

# Mombasa bounding box
lat_center = -4.05
lon_center = 39.67
bbox = [39.6, -4.2, 39.8, -3.9]

if option == "Forest Health":
    st.subheader("🟢 Forest Health Viewer (NDVI)")
    st.markdown("**Monitoring region:** Mombasa County")

    if st.button("Compute NDVI"):
        st.info("Processing Sentinel-2 imagery. This may take a moment...")

        try:
            ndvi = get_ndvi(bbox)
            st.success("NDVI computed successfully!")

            with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as tmp:
                ndvi.rio.to_raster(tmp.name, compress="LZW")
                m = leafmap.Map(center=(lat_center, lon_center), zoom=11)
                m.add_raster(tmp.name, layer_name="NDVI", colormap="Greens", nodata=0)
                m.to_streamlit(height=500)

        except Exception as e:
            st.error(f"Failed to compute NDVI: {str(e)}")

        # Clean up memory
        del ndvi
        gc.collect()

elif option == "Degradation":
    st.subheader("🟠 Forest Degradation Viewer")
    st.markdown("Coming soon: Monitoring gradual canopy loss and forest stress using time-series NDVI/EVI...")

elif option == "Deforestation":
    st.subheader("🔴 Deforestation Viewer")
    st.markdown("Coming soon: Detecting abrupt forest clearing using Sentinel-2 or Landsat change detection...")

elif option == "Fire":
    st.subheader("🔥 Fire Monitoring")
    st.markdown("Coming soon: Burn area detection and active fire alerts using MODIS/VIIRS thermal data...")
