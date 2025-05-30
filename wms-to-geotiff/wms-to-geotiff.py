#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "OWSLib",
#     "rasterio",
#     "typer",
# ]
# ///

import io
from pathlib import Path
import typer
from typing_extensions import Annotated
from typing import List

import logging

import rasterio
from owslib import wms


def get_image(server, layer, bbox, size, epsg, image_format, transparent, version):
    wms_server = wms.WebMapService(server, version=version)
    img = wms_server.getmap(
        layers=[layer],
        srs=f"EPSG:{epsg}",
        bbox=bbox,
        size=size,
        format=image_format,
        transparent=True,
    )
    return io.BytesIO(img.read())


def convert_image_to_geotiff(image, bbox, epsg, cog):
    with rasterio.open(image) as src:
        profile = src.meta
        profile.update(
            {
                "driver": "COG" if cog else "GTiff",
                "transform": rasterio.transform.from_bounds(
                    *bbox, width=src.width, height=src.height
                ),
                "crs": rasterio.CRS.from_epsg(epsg),
            }
        )
        output = io.BytesIO()
        with rasterio.open(
            output,
            "w",
            **profile,
        ) as out:
            out.write(src.read())
        return output


def main(
    output: Annotated[
        Path,
        typer.Option(
            file_okay=True,
            dir_okay=False,
            writable=True,
        ),
    ],
    server: str,
    layer: str,
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
    width: int,
    height: int,
    epsg: int = 4326,
    image_format: str = "image/png",
    transparent: bool = True,
    version: str = "1.1.1",
    cog: bool = False,
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
    bbox = (x_min, y_min, x_max, y_max)
    size = (width, height)
    image = get_image(
        server, layer, bbox, size, epsg, image_format, transparent, version
    )
    geotiff = convert_image_to_geotiff(image, bbox, epsg, cog)
    with open(output, "wb") as f:
        f.write(geotiff.getbuffer())


if __name__ == "__main__":
    typer.run(main)
