# MDB2Duck
MDB2Duck is a small utility script to convert MS Access Databases to DuckDB Database files.

## Requirements
- Nix
- Direnv (optional)

## Usage
```bash
./mdb2duck.sh File.mdb
```

## Notes
- The resulting file will not always have the correct data types
- The foreign keys and the constrainsts are not imported
