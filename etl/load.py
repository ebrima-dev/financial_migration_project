# Inserts data into target DB
from sqlalchemy import create_engine, Table, MetaData, insert
from sqlalchemy.orm import sessionmaker

# Setup the database engine and session
# engine = create_engine('postgresql://postgres:yourpass@localhost:5432/modern_financials')
# Session = sessionmaker(bind=engine)

# def load_journal_entries(df):
#     metadata = MetaData(bind=engine)
#     metadata.reflect(only=['journal_entries'])
#     journal_entries = metadata.tables['journal_entries']

#     session = Session()
#     try:
#         # Insert rows inside a transaction
#         for _, row in df.iterrows():
#             stmt = insert(journal_entries).values(
#                 transaction_id=row['txn_id'],
#                 account_id=row['account_id'],
#                 debit_amount=row['dr_amt'],
#                 credit_amount=row['cr_amt'],
#                 currency=row['currency']
#             )
#             session.execute(stmt)
#         session.commit()
#     except Exception as e:
#         session.rollback()
#         print(f"Error loading journal entries: {e}")
#         raise
#     finally:
#         session.close()

PG_CONN = "postgresql://postgres:pgpass@localhost:5432/modern_financials"
engine = create_engine(PG_CONN)
Session = sessionmaker(bind=engine)

def _load_table(df, table_name, mapping):
    metadata = MetaData()
    metadata.reflect(bind=engine, only=[table_name])
    table = metadata.tables[table_name]

    session = Session()
    try:
        for _, row in df.iterrows():
            stmt = insert(table).values({col: row[src] for col, src in mapping.items()})
            session.execute(stmt)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error loading {table_name}: {e}")
        raise
    finally:
        session.close()

def load_journal_entries(df):
    mapping = {
        'transaction_id': 'txn_id',
        'account_id': 'account_id',
        'debit_amount': 'dr_amt',
        'credit_amount': 'cr_amt',
        'currency': 'currency'
    }
    _load_table(df, 'journal_entries', mapping)

def load_transactions(df):
    print("Transaction DF columns:", df.columns)
    mapping = {
        "transaction_id": "pay_id",
        "description": "description",
        # "transaction_date": "txn_date",
    }
    _load_table(df, "transactions", mapping)

def load_parties(df):
    mapping = {
        "party_id": "party_id",
        "name": "name",
        "party_type": "party_type"
    }
    _load_table(df, "parties", mapping)