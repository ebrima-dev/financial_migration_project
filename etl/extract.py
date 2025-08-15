# Pulls data from source DB
import pymysql
import pandas as pd

# def extract_ledger_entries():
#     conn = pymysql.connect(host='localhost', user='root', password='yourpass', db='legacy_financial') 
#     query = """
#             SELECT le.txn_id, le.txn_dt, le.acct_id, a.acct_code, a.acct_name,
#             le.dr_amt, le.cr_amt, le.currency
#             FROM ledger_entries le
#             JOIN acct_tbl a on le.acct_id = a.acct_id;
#             """               
#     df = pd.read_sql(query, conn)
#     conn.close()
#     return df


# Put in an environment variable or config file to hold this later
MYSQL_CONN = {
        "host": "localhost",
        "user": "root",
        "password": "rootpass",
        "db": "legacy_financials"
}

def extract_ledger_data():
    conn = pymysql.connect(**MYSQL_CONN)
    
    ledger_df = pd.read_sql("SELECT * FROM ledger_entries;", conn)
    transactions_df = pd.read_sql("SELECT * FROM pay_tbl;", conn)
    # Hard coded party type for now
    parties_df = pd.read_sql("SELECT vend_id AS party_id, vend_nm AS name, 'VENDOR' AS party_type, vend_addr, vend_phone FROM vend_mstr;", conn)
 
    conn.close()
    return ledger_df, transactions_df, parties_df

