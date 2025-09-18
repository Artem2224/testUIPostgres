from sqlalchemy import create_engine,text
from sqlalchemy.exc import SQLAlchemyError

def create_connection(user,password,host, port, database):
    conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(conn_str, echo=True, future=True)

    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        return engine
    except SQLAlchemyError as e:
        raise ConnectionError(f'Ошибка подключения: {e}')