# Cleans, maps, and normalizes data

import pandas as pd

def load_mappings():
    account_map_df = pd.read_csv('mappings/account_code_mapping.csv')
    party_map_df = pd.read_csv('mappings/party_mapping.csv')

    # Convert to dictionaries for quick lookup
    account_map = dict(zip(account_map_df['old_code'], account_map_df['new_code']))
    party_map = dict(zip(party_map_df['old_party_id'], party_map_df['new_party_id']))

    return account_map, party_map

def transform_ledger(df, account_map, party_map):
    """
    Apply transformations to the ledger dataframe:
    - Map old account codes to new account codes
    - Map old party IDs to new party IDs
    """ 
    df['new_account_code'] = df['acct_code'].map(account_map)
    df['new_party_id'] = df['party_id'].map(party_map)

    # Currency conversion (USD->CAD 1.3 rate)
    df['dr_amt'] = df.apply(lambda row: row['dr_amt']*1.3 if row['currency']=='USD' else row['dr_amt'], axis=1)
    df['cr_amt'] = df.apply(lambda row: row['cr_amt']*1.3 if row['currency']=='USD' else row['cr_amt'], axis=1)

    return df

