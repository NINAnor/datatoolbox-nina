import logging
import pathlib
import subprocess

import click
import fiona
from fiona.crs import CRS

logging.basicConfig(level=(logging.INFO))


def gpkg_split(source_file: pathlib.Path, layer: str, wd: pathlib.Path) -> dict:
    with fiona.open(source_file, layer=layer, mode="r") as src:
        profile = src.profile
        profile["driver"] = "GPKG"

        layer_source_file = wd / f"{layer}.gpkg"
        if not layer_source_file.exists():
            logging.info(
                f"{str(layer_source_file)} not found, it will be extracted with fiona",
            )
            # NOTE: the datasets does not work with P://, it will produce a transaction error
            with fiona.open(
                layer_source_file,
                mode="w",
                layer=layer,
                **profile,
            ) as dst:
                dst.writerecords(src)

        json_file = wd / f"{layer}.json"

        subprocess.run(
            [  # noqa: S603, S607
                "ogr2ogr",
                "-f",
                "GeoJSON",
                "-t_srs",
                "EPSG:4326",
                json_file,
                layer_source_file,
            ],
        )
        profile["driver"] = "GeoJSON"
        profile["crs"] = CRS.from_epsg(4326)
        if not layer_source_file.exists():
            logging.info(
                f"{str(layer_source_file)} not found, it will be extracted with fiona",
            )
            # NOTE: the datasets does not work with P://, it will produce a transaction error
            with fiona.open(
                layer_source_file,
                mode="w",
                layer=layer,
                **profile,
            ) as dst:
                dst.writerecords(src)

        return wd / f"{layer}.json"


@click.command()
@click.argument("gpkg_file", type=click.Path(exists=True))
@click.option('--ignore', '-i', multiple=True)
@click.option(
    "--wd",
    default=".",
    type=click.Path(dir_okay=True, exists=True, readable=True, path_type=pathlib.Path),
)
def run(gpkg_file: pathlib.Path, wd: pathlib.Path, ignore) -> None:
    layers = fiona.listlayers(gpkg_file)

    layers_gjson = []

    if ignore:
        logging.info(f"ignoring to {ignore}")
        layers = list(filter(lambda layer: layer not in ignore, layers))

    logging.info(f"found {layers}")

    for layer in layers:
        logging.info(f"process {layer}")
        result = gpkg_split(gpkg_file, layer, wd)
        layers_gjson.append(result)

    subprocess.run(
        [  # noqa: S603, S607
            "tippecanoe",
            "-zg",
            "--projection=EPSG:4326",
            "--extend-zooms-if-still-dropping",
            "--drop-densest-as-needed",
            "--force",
            "-pk",
            "-o",
            (wd / f"{gpkg_file}.pmtiles"),
        ]
        + layers_gjson,
    )

    for l in layers_gjson:
        l.unlink()

if __name__ == "__main__":
    run()
