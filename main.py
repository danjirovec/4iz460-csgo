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

# todo add buyable category to items
df_equipment = pd.read_csv("./data/csgo_equipment.csv", sep=',')
df_equipment.head(5)


# todo add buyable category to items
df_weapons = pd.read_csv("./data/csgo_weapons.csv", sep=',')
df_weapons.head(5)


def df_to_dict(df_to_convert: pd.DataFrame, key: str, value: str) -> dict:
    return {x[key]:x[value] for x in df_to_convert.to_dict(orient='records')}

equipment_trans = df_to_dict(df_equipment, key='name', value='price')
equipment_weapons = df_to_dict(df_weapons, key='Name', value='Cost')
# todo add buyable to category translation dicts

def parse_snapshot_column_to_buyable(row: pd.Series, trans: dict) -> tuple(str, str):


    return buyable_type, buyable_category, buyable_proper_name