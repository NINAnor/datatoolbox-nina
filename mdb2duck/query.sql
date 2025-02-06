
create or replace table "$TABLENAME" AS SELECT * FROM read_ndjson("${TABLENAME}.json")
