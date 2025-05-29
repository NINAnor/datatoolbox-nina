#!/bin/bash
set -euo pipefail

get_features_for_tippercanoe() {
    ogr2ogr -of GeoJSONSeq -dsco RS=YES -t_srs EPSG:4326 \
        -mapFieldType Date=String /vsistdout/ "$1" "$2" |
        jq -c --arg layer "$2" '.tippecanoe.layer = $layer'
}
export -f get_features_for_tippercanoe

source="$1"
temporary="$(dirname $(realpath $source))"
ogrinfo -json "$source" | jq -r .layers[].name |
    parallel --line-buffer -- get_features_for_tippercanoe "$source" "{}" |
    tippecanoe --force -t "$temporary" -o "${source%.*}.pmtiles" \
        -zg --drop-densest-as-needed --extend-zooms-if-still-dropping -pk
