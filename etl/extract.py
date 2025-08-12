# Pulls data from source DB
import pymsql
import pandas as pd

def extract_ledger_entries():
    conn = pymysql.connect(host='localhost', user='root', password='yourpass', db='legacy_financial') 
    query = """
            SELECT le.txn_id, le.txn_dt, le.acct_id, a.acct_code, a.acct_name,
            le.dr_amt, le.cr_amt, le.currency
            FROM ledger_entries le
            JOIN acct_tbl a on le.acct_id = a.acct_id;
            """               
    df = pd.read_sql(query, conn)
    conn.close()
    return df