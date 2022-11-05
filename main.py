"""
Stejny kod jako v notebooku, pouze ve forme skriptu
"""

import numpy as np
import pandas as pd
import cleverminer as clm
import os

os.chdir(r"F:/School/Magistr/3. semestr/Pokročilé přístupy k dobývání znalostí z databází 4IZ460/semestralni_prace/4iz460-csgo")

df = pd.read_csv("./data/csgo_round_snapshots.csv", sep=',')
df.head(5)

columns = df.columns.tolist()

df_equipment = pd.read_csv("./data/csgo_equipment.csv", sep=',')
df_equipment.head(5)

df_weapons = pd.read_csv("./data/csgo_weapons.csv", sep=',')
# rename name and price columns, so it has same convention for the columns we're going to use as equipment
df_weapons = df_weapons.rename(columns={'Name': 'name', 'Cost': 'price'})
df_weapons.head(5)

df_buyable_trans = pd.read_csv("./data/csgo_byuable_to_category_nickname.csv", sep=',')
df_buyable_trans.head(5)

# put weapons and equipment together
df_buyables = pd.concat([df_equipment, df_weapons], ignore_index=True)
# join buyables with categories
df_buyables = df_buyables.merge(df_buyable_trans, on='name')
# keep only the columns we plan to use
df_buyables = df_buyables.loc[:, ['name', 'price', 'category', 'nickname']]
# clean price values
df_buyables['price'] = df_buyables['price'].str.replace('$', '', regex=False).astype(int)


def df_to_dict(df_to_convert: pd.DataFrame, key: str, value: str | list) -> dict:
    """
    This function takes a dataframe, and creates a dictionary, where the keys will be values from key, and value will
    be either a single value (if value parameter is string), or a dictionary, where the keys will be values from value
    (which is a list in this scenario), and the dictionary values will be values in columns in list.

    Parameters
    ----------
    df_to_convert: pd.DataFrame
    key: str
    value: str | list

    Returns
    -------
    dict
    """
    return {x[key]: x[value] if isinstance(value, str) else {xkey: x[xkey] for xkey in value} for x in df_to_convert.to_dict(orient='records')}


buyables_trans = df_to_dict(df_buyables, key='nickname', value=['price', 'category'])

def parse_snapshot_column_to_buyable(row: pd.Series, trans: dict) -> tuple[str, str]:

    # count t and ct weapons
    # count t and ct categories
    # count t and ct equipment / weapons
    # count overall investment

    return buyable_type, buyable_category, buyable_proper_name


s_cols = df.columns.tolist()
[x for x in s_cols if x.startswith('t_')]