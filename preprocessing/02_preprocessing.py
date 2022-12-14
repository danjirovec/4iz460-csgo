"""
Code for preprocessing input data
"""

import pandas as pd
from preprocessing_functions import df_to_dict, parse_snapshot_column_to_buyable, create_match_quarters_no_beginnings
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

"""
Read and show what files look like
"""
logger.info("Reading files")

# main file containing round snapshots
df = pd.read_csv("./data/csgo_round_snapshots.csv", sep=',')
df.head(5)

# file containing names and prices of equipment
df_equipment = pd.read_csv("./data/csgo_equipment.csv", sep=',')
df_equipment.head(5)

# file containing names and prices of weapons (also other columns, which we will not use)
df_weapons = pd.read_csv("./data/csgo_weapons.csv", sep=',')
# rename name and price columns, so it has same convention for the columns we're going to use as equipment
df_weapons = df_weapons.rename(columns={'Name': 'name', 'Cost': 'price'})
df_weapons.head(5)

# load file created by helper_scripts/generate_buyable_categories.py
# it contains buyable name, nickname (used in snapshots), and category
df_buyable_trans = pd.read_csv("./data/csgo_byuable_to_category_nickname.csv", sep=',')
df_buyable_trans.head(5)


logger.info("Creating trans dictionary")
# put weapons and equipment together into one dataframe
df_buyables = pd.concat([df_equipment, df_weapons], ignore_index=True)
# join buyables with categories on name
df_buyables = df_buyables.merge(df_buyable_trans, on='name')
# keep only the columns we plan to use
df_buyables = df_buyables.loc[:, ['name', 'price', 'category', 'nickname']]
# clean price values, so it's int, and we can do math on it
df_buyables['price'] = df_buyables['price'].str.replace('$', '', regex=False).astype(int)

# create translation dict from nickanme to buyable price and category
buyables_trans = df_to_dict(df_buyables, key='nickname', value=['price', 'category'])

# these columns will be used for automatically calculating buyable price information
auto_columns = [x for x in df.columns.tolist() if x.startswith(('ct_weapon', 't_weapon', 'ct_grenade', 't_grenade'))]

logger.info("Parsing snapshot columns")
# create dicts with new price information in a new column called buyable_dict
df['buyable_dict'] = df.apply(lambda x: parse_snapshot_column_to_buyable(row=x, trans=buyables_trans,
                                                                         automatic_columns=auto_columns),
                              axis=1)


logger.info("Creating price columns")
# create dataframe columns from newly created column, drop that column and concat new dataframe to existing snapshot
# fill nas with zeros - not every dict has every column, so make sure math is fine later on
df = pd.concat([df.drop(columns=['buyable_dict']), df['buyable_dict'].apply(pd.Series).fillna(0)], axis=1)


logger.info("Calculating new simple attributes")
# calculate player surplus
df['ct_players_alive_surplus'] = df['ct_players_alive'] - df['t_players_alive']

# categorize time
df['time_left'].describe()
df['time_left_cat'] = pd.cut(df['time_left'], bins=3, labels=['late', 'mid', 'early'])

# calculate overall players alive
df['players_alive'] = df['ct_players_alive'] + df['t_players_alive']

# calculate round number
# +1 because in first round, score is 0:0
df['round_number'] = df['ct_score'] + df['t_score'] + 1

# calculate match quarters
df['match_quarters'] = df['round_number'].apply(create_match_quarters_no_beginnings)

logger.info("Saving dataset")
# save processed dataset
df.to_csv("./data/csgo_round_snapshots_processed.csv", index=False)
logger.info("Done!")