#!/bin/bash
set -euo pipefail

source="$1"

gdal_translate  $source "$source.cog" -co NUM_THREADS=ALL_CPUS -of COG -co OVERVIEWS=AUTO -co BIGTIFF=IF_SAFER -co COMPRESS=ZSTD
