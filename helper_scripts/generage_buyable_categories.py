"""
This script helps create data that originally weren't part of the downloaded files.
"""

import pandas as pd
import os
import logging

logger = logging.getLogger()

os.chdir(r"F:/School/Magistr/3. semestr/Pokročilé přístupy k dobývání znalostí z databází 4IZ460/semestralni_prace/4iz460-csgo")


"""
Generate categories for weapons
"""
df_weapons = pd.read_csv("./data/csgo_weapons.csv", sep=',')
# pre-generate the dictionary to manually fill the categories below
# weapons_to_categories = {x: 'something' for x in df_weapons['Name'].tolist()}

weapons_to_categories = {
    'AK-47': 'rifle',
    'AUG': 'rifle',
    'AWP': 'sniper',
    'CZ75 Auto': 'pistol',
    'Desert Eagle': 'pistol',
    'Dual Berettas': 'pistol',
    'FAMAS': 'rifle',
    'Five-SeveN': 'pistol',
    'G3SG1': 'sniper',
    'Galil AR': 'rifle',
    'Glock 18': 'pistol',
    'M249': 'machine gun',
    'M4A4': 'rifle',
    'M4A1-S': 'rifle',
    'MAC-10': 'smg',
    'MAG-7': 'shotgun',
    'MP7': 'smg',
    'MP9': 'smg',
    'Negev': 'machine gun',
    'Nova': 'shotgun',
    'P2000': 'pistol',
    'P250': 'pistol',
    'P90': 'smg',
    'PP-Bizon': 'smg',
    'Sawed-Off': 'shotgun',
    'SCAR-20': 'sniper',
    'SG 553': 'rifle',
    'SSG 08': 'sniper',
    'Tec-9': 'pistol',
    'UMP-45': 'smg',
    'USP-S': 'pistol',
    'XM1014': 'shotgun'
}

weapons_df_names = df_weapons['Name'].tolist()

# check that all weapons are covered
if not all([x in weapons_to_categories for x in weapons_df_names]):
    missing_guns = [x for x in weapons_df_names if x not in weapons_to_categories]
    raise AttributeError(f"Following guns not covered in dict, it needs to be updated! - {missing_guns}")

# check for gun redundancy
if not all([x in weapons_df_names for x in weapons_to_categories.keys()]):
    redundant_guns = [x for x in weapons_to_categories.keys() if x not in weapons_df_names]
    logger.warning(f"Following guns redundant in dict, it should be updated! - {redundant_guns}")

"""
Generate categories for equipment
"""
df_equipment = pd.read_csv("./data/csgo_equipment.csv", sep=',')
# pre-generate the dictionary to manually fill the categories below
equipment_to_categories = {x: 'something' for x in df_equipment['name'].tolist()}
equipment_to_categories = {
    'Kevlar Vest': 'armor',
    'Kevlar Vest + Helmet': 'armor',
    'Zeus x27': 'CT equipment',
    'Defuse Kit': 'CT equipment',
    'Molotov': 'grenade',
    'Incendiary Grenade': 'grenade',
    'Decoy Grenade': 'grenade',
    'Flashbang': 'grenade',
    'HE Grenade': 'grenade',
    'Smoke Grenade': 'grenade'
}


equipment_df_names = df_equipment['name'].tolist()

# check that all equipment is covered
if not all([x in equipment_to_categories for x in equipment_df_names]):
    missing_equipment = [x for x in equipment_df_names if x not in equipment_to_categories]
    raise AttributeError(f"Following equipment not covered in dict, it needs to be updated! - {missing_equipment}")

# check for equipment redundancy
if not all([x in equipment_df_names for x in equipment_to_categories.keys()]):
    redundant_equipment = [x for x in equipment_to_categories.keys() if x not in equipment_df_names]
    logger.warning(f"Following equipment redundant in dict, it should be updated! - {redundant_equipment}")

# merge dicts, create a df from them, save as csv
buyable_categories = weapons_to_categories | equipment_to_categories
byuable_categories_df = pd.DataFrame({'name': list(buyable_categories.keys()),
                                      'category': list(buyable_categories.values())})
byuable_categories_df.to_csv("./data/csgo_byuable_to_category.csv", index=False)
