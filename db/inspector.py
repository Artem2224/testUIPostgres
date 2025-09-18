from sqlalchemy import inspect

def get_tables(engine):
    inspector = inspect(engine)
    return inspector.get_table_names()

def get_columns(engine, table_name):
    inspector = inspect(engine)
    return inspector.get_columns(table_name)