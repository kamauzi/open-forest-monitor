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
    ds = load(items, bands=["red", "nir"], bbox=bbox, resolution=10, groupby="solar_day").compute()
    ds = ds.coarsen(x=2, y=2, boundary="trim").mean()  # Optional downsample
    ndvi = (ds.nir - ds.red) / (ds.nir + ds.red)
    return ndvi.median(dim="time").rio.write_crs("EPSG:32637")
