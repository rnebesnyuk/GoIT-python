from connect import create_connection
from psycopg2 import DatabaseError


def create_table(conn, sql_script):
    with open(sql_script) as f:
        script = f.read()
    try:
        c = conn.cursor()
        c.execute(script)
        c.close()
    except DatabaseError as e:
        print(e)



if __name__ == "__main__":
    with create_connection() as conn:
        if conn is not None:
            create_table(conn, 'tables.sql')
