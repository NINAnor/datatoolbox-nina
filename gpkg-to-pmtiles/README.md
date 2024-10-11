# GPKG to PMTiles
A script to convert a GPKG dataset to PMTiles using GDAL and Tippecanoe.

This script will split each layer into a separate gpkg file, then convert each to GeoJSON and use `tippecanoe` to generate a PMTiles with all the layers together.


# Usage
```bash
nix-shell
gpkg-to-pmtiles my-file.gpkg --wd /my/working/directory
```

**NOTE**: GPKG have errors while using them on network storages such as P: or R:, use `/data/scratch` in case
