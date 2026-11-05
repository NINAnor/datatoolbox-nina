#!/bin/bash
set -eu

source="$1"

exec gdal raster convert --of COG --co NUM_THREADS=ALL_CPUS --co BIGTIFF=IF_SAFER --co COMPRESS=ZSTD --co PREDICTOR=YES "$source" "${source%.*}.cog.tif"
