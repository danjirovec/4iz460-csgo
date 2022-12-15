"""
This file contains function used in preprocessing data, so it can be used for data mining
"""

import pandas as pd
import math
from collections import defaultdict


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
    return {x[key]: x[value] if isinstance(value, str) else {xkey: x[xkey] for xkey in value}
            for x in df_to_convert.to_dict(orient='records')}


def parse_snapshot_column_to_buyable(row: pd.Series, trans: dict, automatic_columns: list[str]) -> dict:
    """
    This function computes prices for all buyables (any equipment that can be bought) in each team. Prices are computed
    for each buyable (e.g. a sum of what it would cost whole team to buy all incendiary grenades or AK74s they have on
    them), category (e.g. cost of all grenades, armor, rifles), and overall spend (sum of all equipment being held).
    Along the prices, amounts of items in a category (grenades, shotguns, etc) are also calculated.


    Parameters
    ----------
    row: pd.Series
        pandas series corresponding to each row in snapshot dataset. It holds information of how many items of each type
        the team members hold

    trans: dict
        dictionary, whose keys correspond to buyable nickname
                    the values under each key is a dictionary with price and category information for buyable

    automatic_columns: list[str]
        list of columns, that can be automatically read. Corresponds to all weapon and grenade columns in the format of
        '{TEAM}_{WEAPON/GRENADE}_{BUYABLE_NICKNAME}'

    Returns
    -------
    dict
        dictionary containing price info as described in function description
    """

    # create default int dict - will not throw an error when referring to keys that do not exist
    new_cols = defaultdict(int)

    # handle weapons and grenades
    for col in automatic_columns:
        value = row[col]
        if value > 0:
            buyable_name = col.split('_')  # get all portions of column name - (team, weapon/grenade, nickname)
            buyable_price = trans[buyable_name[-1]]['price'] * value  # ger price for whole team
            new_cols[f'{col}_price'] = buyable_price  # price for specific item
            # add item price to category and overall spend
            new_cols[f'{buyable_name[0]}_category_{trans[buyable_name[-1]]["category"]}_price'] += buyable_price
            new_cols[f'{buyable_name[0]}_category_{trans[buyable_name[-1]]["category"]}_amount'] += value
            new_cols[f'{buyable_name[0]}_overall_investment'] += buyable_price

    # handle defuse kits
    defuse_kits = row['ct_defuse_kits']
    if defuse_kits > 0:
        # defuse kits are not a category, so only add to item spend and overall spend
        defuse_kits_price = defuse_kits * trans['defuse']['price']
        new_cols[f'ct_defuse_kits_price'] = defuse_kits_price
        new_cols[f'ct_overall_investment'] += defuse_kits_price

    # handle armor
    teams = ['t', 'ct']
    # do the same action for each team
    for team in teams:
        helmets = row[f'{team}_helmets']
        # vests calculated based on overall points available (minimal count estimate)
        vests = math.ceil(row[f'{team}_armor'] / 100)

        # kevlar without helmet = kevlar in general - amount of helmets
        kevlar_price = (vests - helmets) * trans['kevlar']['price']
        kevlarhelmet_price = helmets * trans['kevlarhelmet']['price']

        # add prices for each item, category, and overall spend
        new_cols[f'{team}_kevlar_price'] = kevlar_price
        new_cols[f'{team}_kevlarhelmet_price'] = kevlarhelmet_price
        new_cols[f'{team}_category_armor_price'] = kevlar_price + kevlarhelmet_price
        new_cols[f'{team}_overall_investment'] += kevlar_price + kevlarhelmet_price

    return new_cols


def create_match_quarters_no_beginnings(round_number: int) -> int:
    """
    This function creates match quarters. These are defined as at most 30 rounds, without beginning rounds of each half.
    Quarters created as [2,8], [9,15], [17,23], [24,30]
    
    Parameters
    ----------
    round_number: int
        match round number

    Returns
    -------
    match quarter: int
        quarter which the match is in. If the round number doesn't match (either first round of each half or overtime),
            -1 is returned
    """

    if (round_number >= 2) & (round_number <= 8):
        return 1
    elif (round_number >= 9) & (round_number <= 15):
        return 2
    elif (round_number >= 17) & (round_number <= 23):
        return 3
    elif (round_number >= 24) & (round_number <= 30):
        return 4
    else:
        return -1


