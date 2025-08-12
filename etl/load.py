# Inserts data into target DB
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import insert
from sqlalchemy.orm import sessionmaker

# Setup the database engine and session
engine = create_engine('postgresql://postgres:yourpass@localhost:5432/modern_financials')
Session = sessionmaker(bind=engine)

def load_journal_entries(df):
    metadata = MetaData(bind=engine)
    metadata.reflect(only=['journal_entries'])
    journal_entries = metadata.tables['journal_entries']

    session = Session()
    try:
        # Insert rows inside a transaction
        for _, row in df.iterrows():
            stmt = insert(journal_entries).values(
                transaction_id=row['txn_id'],
                account_id=row['account_id'],
                debit_amount=row['dr_amt'],
                credit_amount=row['cr_amt'],
                currency=row['currency']
            )
            session.execute(stmt)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error loading journal entries: {e}")
        raise
    finally:
        session.close()