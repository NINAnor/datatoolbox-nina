#!/bin/bash

grass_meta_to_parquet() {
    find /data/grass/$1/$2/ -regextype posix-extended -regex '.*/(cellhd|cell)/.*' -exec realpath {} + > rasters
    find /data/grass/$1/$2/ -regextype posix-extended -regex '.*/vector/.*/head$' -exec realpath {} + > vectors
    parallel --resume-failed --joblog log-raster --results data/type=raster gdalinfo '{}' -json :::: rasters
    parallel --resume-failed --joblog log-vector --results data/type=vector ogrinfo '{}' -json :::: vectors
    duckdb ':memory:' "copy (select (json::json).description::varchar as file, json as metadata from read_json_objects('data/*/1/*/stdout', format='unstructured')) to 'grass.parquet'"
}
