

`wms-to-geotiff` presents two ways to fetches the requested bounding box from a WMS layer and save it as a GeoTIFF file:
- using `wms-to-geotiff.py`, a custom script which provides a simple command line interface and can be reused in Python scripts
- using `gdal_translate`, provided by the GDAL official project

## wms-to-geotiff.py

Example:

```bash
wms-to-geotiff.py "https://wms.geonorge.no/skwms1/wms.nib" ortofoto 9.705 59.035 9.707 59.037 300 250 --output output.geotiff
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
gdal_translate -of GTiff -outsize 300 250 "WMS:https://wms.geonorge.no/skwms1/wms.nib?service=WMS&version=1.1.1&request=GetMap&layers=ortofoto&styles=&width=300&height=250&srs=EPSG:4326&bbox=9.705,59.035,9.707,59.037&format=image/png&transparent=TRUE" output.geotiff
```

Such long output URL can be optained by running `wms-to-geotiff` with the `--verbose` option, which prints all the web requests, as well as additional details.

Replace `-of GTiff` with `-of COG` to generate a [Cloud Optimized GeoTIFF](https://gdal.org/en/stable/drivers/raster/cog.html) raster.
