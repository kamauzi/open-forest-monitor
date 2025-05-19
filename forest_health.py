# forest_health.py
from odc.stac import load
import planetary_computer
import pystac_client
import xarray as xr

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
    ).persist()
    ndvi = (ds.nir - ds.red) / (ds.nir + ds.red)
    return ndvi.median(dim="time")
