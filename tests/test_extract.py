import pymysql
import pandas as pd

# This script connects to a MySQL database and retrieves data from a table named 'ledger_entries'.
def read_mysql_test():
    conn = pymysql.connect(host='localhost', user='root', password='rootpass', db='legacy_financials')

    query = "SELECT * FROM ledger_entries LIMIT 5;"

    df = pd.read_sql(query, conn)
    print(df.head())

    conn.close()