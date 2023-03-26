from psycopg2 import connect, Error
from contextlib import contextmanager


@contextmanager
def create_connection():
    """create a database connection to a Postgres database"""
    conn = None
    try:
        conn = connect(
            host="dumbo.db.elephantsql.com",
            user="bggqkxky",
            password="EElLec4qqLeZ_e6NEvwEOVtnXPNq9Fm-",
            database="bggqkxky",
            port=5432,
        )
        yield conn
        conn.commit()
    except Error as err:
        print(err)
        conn.rollback()
    finally:
        if conn:
            conn.close()
