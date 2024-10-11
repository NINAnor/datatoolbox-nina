# CSV difference
This script allows to find and explore difference between CSV files.

The comparison is done without reading the header, this means that both the files should have the same structure.


**NOTE**: to use this script both the CSV files should be encoded as UTF-8, this can be achived on GNU Linux with `iconv`.

## Install
```
nix-shell
csv-diff --help
csv-diff target/path source/path
```
