# Vector to PMTiles
A script to convert a vector dataset to PMTiles using GDAL and Tippecanoe.


# Usage
```bash
nix-shell
vector-to-pmtiles my-file.gpkg
```

**NOTE**: the resulting file is saved in the same directory of the vector file, as well as the temporary files.

# Example

Produce multiple layers based on a column value:
```bash
parallel -j1 --bar -- ogr2ogr -append -where year="{}" -nln "{}" -t_srs EPSG:4326 nedbygging_norge_2017_2024.gpkg nedbygging_norge_2017_2024.geojson ::: {2018..2024}
```
```bash
./vector-to-pmtiles.sh nedbygging_norge_2017_2024.gpkg
```

Resulting file: `nedbygging_norge_2017_2024.pmtiles`
