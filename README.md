# Data Toolbox
This repository aims to collect and store useful scripts to process/manage/engineer data.

## Setup

This project uses [Pixi](https://pixi.sh) for dependency management.

### Install Pixi

If you don't have Pixi installed, install it with:

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

### Install Dependencies

Once Pixi is installed, run:

```bash
pixi install
```

This will install all required dependencies including GDAL, tippecanoe, and parallel.

### Run Tasks

You can run available tasks using:

```bash
pixi run <task-name>
```

For example:
```bash
pixi run vector-to-pmtiles <input-file>
```
