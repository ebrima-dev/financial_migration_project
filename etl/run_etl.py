import pandas as pd
from sqlalchemy import create_engine
from extract import extract_ledger_data
from transform import load_mappings, transform_ledger
from load import load_journal_entries, load_transactions, load_parties

def run_etl():
    print("Starting ETL process...")

    # Step 1: Extract data from legacy MySQL database
    print("Extracting data from MySQL...")
    ledger_df, transactions_df, parties_df = extract_ledger_data()

    # Step 2: Load mappings & transform
    print("Loading mapping tables...")
    account_map, party_map = load_mappings()

    print("Transforming ledger data...")
    print(ledger_df.columns)  # Debugging line to check the initial data 
    transformed_ledger = transform_ledger(ledger_df, account_map, party_map)

    # (Add similar transform functions if needed for transactions and parties)

    # Step 3: Load transformed data into PostgreSQL
    print("Loading data into PostgreSQL...")
    load_parties(parties_df)
    load_transactions(transactions_df)
    load_journal_entries(transformed_ledger)
 

    print("ETL process completed successfully!")

if __name__ == "__main__":
    run_etl()