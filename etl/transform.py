# Cleans, maps, and normalizes data
import os
import pandas as pd

def test_file_exists(file_path):
    try:
        pd.read_csv(file_path)
        return True
    except FileNotFoundError:
        return False

def load_mappings():
    account_map_df = pd.read_csv('../mappings/account_code_mapping.csv').set_index("old_code")["new_code"].to_dict()
    party_map_df = pd.read_csv('../mappings/party_mapping.csv').set_index("old_party_id")["new_party_id"].to_dict()

    return account_map_df, party_map_df

def transform_ledger(df, account_map, party_map):
    # To handle NaN values in account id - we set them to 0 if Na
    df["account_id"] = df["acct_id"].map(account_map).fillna(0).astype('Int64')
    print("In Here!")
    print(df.columns)
    # Alternative to setting account_id to 0 is if we drop rows with missing foreign keys:
    df = df.dropna(subset=["account_id", "txn_id"])

    """No party ID key in the ledger. It comes from the vendr master
        table. May have to log that information at some point. 
    """
    # df["party_id"] = df["party_id"].map(party_map)
    
    return df

    # Convert to dictionaries for quick lookup
    # account_map = dict(zip(account_map_df['old_code'], account_map_df['new_code']))
    # party_map = dict(zip(party_map_df['old_party_id'], party_map_df['new_party_id']))

    # return account_map, party_map

# def transform_ledger(df, account_map, party_map):
#     """
#     Apply transformations to the ledger dataframe:
#     - Map old account codes to new account codes
#     - Map old party IDs to new party IDs
#     """ 
#     df['new_account_code'] = df['acct_code'].map(account_map)
#     df['new_party_id'] = df['party_id'].map(party_map)

#     # Currency conversion (USD->CAD 1.3 rate)
#     df['dr_amt'] = df.apply(lambda row: row['dr_amt']*1.3 if row['currency']=='USD' else row['dr_amt'], axis=1)
#     df['cr_amt'] = df.apply(lambda row: row['cr_amt']*1.3 if row['currency']=='USD' else row['cr_amt'], axis=1)

#     return df

