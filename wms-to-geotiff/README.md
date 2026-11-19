

`wms-to-geotiff` presents two ways to fetches the requested bounding box from a WMS layer and save it as a GeoTIFF file:
- using `wms-to-geotiff.py`, a custom script which provides a simple command line interface and can be reused in Python scripts
- using `gdal raster`, the GDAL official project's unified command line interface

## wms-to-geotiff.py

Example:

```bash
wms-to-geotiff.py "https://nib-proxy.nina.no/ortofoto/service" ortofoto 9.705 59.035 9.707 59.037 300 250 --output output.geotiff
```

Since the script requires some additional dependencies, such as rasterio (which includes the GDAL library), it is recommended to start the script using [uv](https://docs.astral.sh/uv).

Example:
```bash
uv run wms-to-geotiff.py --help
```

Use `--cog` to generate a [Cloud Optimized GeoTIFF](https://gdal.org/en/stable/drivers/raster/cog.html) raster, and `--verbose` to show all the web requests and debug information.

## GDAL

Example:

```bash
gdal raster pipeline 'read "WMS:https://nib-proxy.nina.no/ortofoto/service?service=WMS&version=1.1.1&request=GetMap&layers=ortofoto&styles=&width=300&height=250&srs=EPSG:4326&bbox=9.705,59.035,9.707,59.037&format=image/png&transparent=TRUE" ! resize --size 300,250 ! write output.geotiff --of GTiff'
```

Such long output URL can be obtained by running `wms-to-geotiff` with the `--verbose` option, which prints all the web requests, as well as additional details.

Replace `--of GTiff` with `--of COG` to generate a [Cloud Optimized GeoTIFF](https://gdal.org/en/stable/drivers/raster/cog.html) raster.

Note: this syntax requires GDAL 3.11 or later, which introduced the unified `gdal raster` command line interface.
