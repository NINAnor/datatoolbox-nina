# GPKG to PMTiles
A script to convert a GPKG dataset to PMTiles using GDAL and Tippecanoe.

This script will split each layer into a separate gpkg file, then convert each to GeoJSON and use `tippecanoe` to generate a PMTiles with all the layers together.


# Usage
```bash
nix-shell
gpkg-to-pmtiles my-file.gpkg --wd /my/working/directory
```

**NOTE**: GPKG have errors while using them on network storages such as P: or R:, use `/data/scratch` in case

# Example:

Produce multiple layers based on a column value:
```bash
parallel -j1 --bar -- ogr2ogr -append -where year="{}" -nln "{}" -t_srs EPSG:4326 nedbygging_norge_2017_2024.gpkg nedbygging_norge_2017_2024.geojson ::: {2018..2024}
```
```bash
./main.py nedbygging_norge_2017_2024.gpkg
```

Resulting file: `nedbygging_norge_2017_2024.gpkg.pmtiles`
Temporary files: `20??.gpkg` (one for each layer)
