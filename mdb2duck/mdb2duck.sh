#! /usr/bin/env nix-shell
#! nix-shell -i bash -p mdbtools duckdb parallel

set -e
export FILENAME=$1

process_table() {
    export TABLENAME=$1
    if [ -z "${TABLENAME}" ]; then
        return
    fi
    echo $TABLENAME
    mdb-json -U $FILENAME $TABLENAME > "${TABLENAME}.json"
    duckdb "$FILENAME.duckdb" "$(envsubst<query.sql)"
    rm "${TABLENAME}.json"
    echo 'Inserted.'
}

export -f process_table

mdb-tables -T $FILENAME | awk '{print $2" "$3}' | parallel -j1 process_table {1} ::::
