import duckdb
import click
import pathlib

@click.command()
@click.argument("result", type=click.Path(exists=True), help="the target file to compare")
@click.argument("source", type=click.Path(exists=True), help="the source file to compare")
@click.argument("id_column_index", default=0, type=str, help="the index of the id column, 0 indexed")
@click.option("--output", default=None, type=click.Path(), help="output diff as csv to this path")
@click.option("--duckdb_file", default=None, type=click.Path(), help="run the processing inside a duckdb")
@click.option("--ignore_columns", default=[], type=list[str], help="ignore this column for the report")
def run(source, result, output, id_column_index, duckdb_file, ignore_columns):
    if duckdb_file:
        pathlib.Path(duckdb_file).unlink()
    conn = duckdb.connect(duckdb_file or ':memory:')
    conn.sql(f"""
             create table "source" as select * from read_csv('{source}', header=false, AUTO_DETECT=true);
            """)
    conn.sql(f"""
             create table "result" as select * from read_csv('{result}', header=false, AUTO_DETECT=true);
            """)


    print("Total columns")
    print(conn.sql("select table_name, count(table_name) as columns from information_schema.columns where table_name in ('source','result') group by table_name"))

    print("Total rows")
    print(conn.sql("(select 'source' as table_name, count(*) as total from source) union (select 'result' as table_name, count(*) as total from result)"))

    columns = [row[0] for row in conn.sql("select column_name from information_schema.columns where table_name = 'source' order by ordinal_position").fetchall()]
    columns_query = [f"ifnull(s.{c}::text, 'NULL')::text = ifnull(r.{c}::text, 'NULL')::text as {c}_diff" for c in columns]

    id_column = columns[id_column_index]

    conn.sql(f"""
        create table diff as (
            select 
                s.{id_column} as oldId,
                r.{id_column} as newId,
                {','.join(columns_query)}
            from "source" as s
            full join "result" as r on s.{id_column} = r.{id_column}
        );
    """)

    conn.sql("create table column_errors (column_name text, diff bool, total int)")

    for c in columns:
        conn.sql(f"""
            insert into column_errors (
                 select '{c}' as column_name, {c}_diff as diff, count({c}_diff) as total from diff where '{c}' not in ({','.join([f"'{v}'" for v in ignore_columns])}) group by {c}_diff)
        """)

    if output:
        conn.sql(f"copy diff to {output} (DELIM '\t')")

    print('Total errors per column')
    print(conn.sql("select * from column_errors where diff is false and total > 0 order by total desc"))

    print('Total')
    query = conn.sql("select diff, sum(total) as total from column_errors group by diff")
    print(query)
    tot = sum([v[1] for v in query.fetchall()])
    print('Success percentage:')
    print(format(1 - (query.fetchone()[1] / tot), ".0%"))

    print("Error comparison by column")
    for (column_name, _diff, _total) in conn.sql("select * from column_errors where diff is false and total > 0 order by total desc").fetchall():
        print(conn.sql(f"select s.{id_column}, s.{column_name}, r.{column_name} from source s full join result r on r.{id_column} = s.{id_column} where ifnull(s.{column_name}::text, 'NULL')::text <> ifnull(r.{column_name}::text, 'NULL')::text"))
    
    conn.close()

if __name__ == "__main__":
    run()
