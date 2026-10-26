from pathlib import Path


def query_from_file(file,name):
    sql_path = Path(rf"{Path(file).resolve().parent.parent}/sql/{name}.sql")
    sql = sql_path.read_text(encoding="utf-8")
    return sql

def insert_as(file, table_name, columns, query_name):
    template = "INSERT INTO {} ({})\n{}"

    return template.format(
        table_name, 
        ', '.join(columns), 
        f"(\n{query_from_file(file, query_name)}\n)"
    )

def insert(table_name, columns, data):
    
    template = "INSERT INTO {} ({}) VALUES \n{}"

    return template.format(
        table_name, 
        ', '.join(columns), 
        ', \n'.join('({})'.format(', '.join(f'{t!r}'for t in tup)) for tup in data)
        )


def truncate(table_name):
    return f'TRUNCATE TABLE {table_name}'