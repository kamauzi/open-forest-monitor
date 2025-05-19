# forest_health.py

import streamlit as st
from odc.stac import load
import planetary_computer
import pystac_client
import xarray as xr

@st.cache_data(show_spinner=True)
def get_ndvi(bbox, time_range=("2023-01-01", "2023-12-31")):
    catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=f"{time_range[0]}/{time_range[1]}",
        query={"eo:cloud_cover": {"lt": 20}},
    )
    items = [planetary_computer.sign(item) for item in search.get_items()]
    ds = load(
        items,
        bands=["red", "nir"],
        bbox=bbox,
        resolution=10,
        groupby="solar_day"
    ).compute()  # compute instead of persist

    ds = ds.coarsen(x=2, y=2, boundary="trim").mean()  # downsample to reduce memory
    ndvi = (ds.nir - ds.red) / (ds.nir + ds.red)
    ndvi = ndvi.median(dim="time")
    return ndvi.rio.write_crs("EPSG:32637")  # set CRS before export
