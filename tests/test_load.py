import psycopg2
import pandas as pd

# This script connects to a MySQL database and retrieves data from a table named 'ledger_entries'.
def load_test():

    conn = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='pgpass',
        dbname='modern_financials'
    )

    # Create a cursor for executing SQL commands
    cur = conn.cursor()

    # INSERT statement
    insert_query = """
        INSERT INTO test_table (id, input_one, input_two)
        VALUES (1,'test_one', 'test_two')
    """

    cur.execute(insert_query)
    conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":
    load_test()