"""
This script helps create data that originally weren't part of the downloaded files.
"""

import pandas as pd
import os
import logging

logger = logging.getLogger()

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
    'MP5-SD': 'smg',
    'MP7': 'smg',
    'MP9': 'smg',
    'Negev': 'machine gun',
    'Nova': 'shotgun',
    'P2000': 'pistol',
    'P250': 'pistol',
    'P90': 'smg',
    'PP-Bizon': 'smg',
    'R8 Revolver': 'pistol',
    'Sawed-Off': 'shotgun',
    'SCAR-20': 'sniper',
    'SG 553': 'rifle',
    'SSG 08': 'sniper',
    'Tec-9': 'pistol',
    'UMP-45': 'smg',
    'USP-S': 'pistol',
    'XM1014': 'shotgun'
}

weapons_to_nicknames = {'AK-47': 'ak47',
                        'AUG': 'aug',
                        'AWP': 'awp',
                        'CZ75 Auto': 'cz75auto',
                        'Desert Eagle': 'deagle',
                        'Dual Berettas': 'elite',
                        'FAMAS': 'famas',
                        'Five-SeveN': 'fiveseven',
                        'G3SG1': 'g3sg1',
                        'Galil AR': 'galilar',
                        'Glock 18': 'glock',
                        'M249': 'm249',
                        'M4A4': 'm4a4',
                        'M4A1-S': 'm4a1s',
                        'MAC-10': 'mac10',
                        'MAG-7': 'mag7',
                        'MP5-SD': 'mp5sd',
                        'MP7': 'mp7',
                        'MP9': 'mp9',
                        'Negev': 'negev',
                        'Nova': 'nova',
                        'P2000': 'p2000',
                        'P250': 'p250',
                        'P90': 'p90',
                        'PP-Bizon': 'bizon',
                        'R8 Revolver': 'r8revolver',
                        'Sawed-Off': 'sawedoff',
                        'SCAR-20': 'scar20',
                        'SG 553': 'sg553',
                        'SSG 08': 'ssg08',
                        'Tec-9': 'tec9',
                        'UMP-45': 'ump45',
                        'USP-S': 'usps',
                        'XM1014': 'xm1014'
                        }

weapons_df_names = df_weapons['Name'].tolist()

# check that all weapons are covered
if not all([x in weapons_to_categories for x in weapons_df_names]):
    missing_guns = [x for x in weapons_df_names if x not in weapons_to_categories]
    raise AttributeError(f"Following guns not covered in categories dict, it needs to be updated! - {missing_guns}")

# check that all weapons are covered
if not all([x in weapons_to_nicknames for x in weapons_df_names]):
    missing_guns = [x for x in weapons_df_names if x not in weapons_to_nicknames]
    raise AttributeError(f"Following guns not covered in nicknames dict, it needs to be updated! - {missing_guns}")

# check for gun redundancy
if not all([x in weapons_df_names for x in weapons_to_categories.keys()]):
    redundant_guns = [x for x in weapons_to_categories.keys() if x not in weapons_df_names]
    logger.warning(f"Following guns redundant in categories dict, it should be updated! - {redundant_guns}")


# check for gun redundancy
if not all([x in weapons_df_names for x in weapons_to_nicknames.keys()]):
    redundant_guns = [x for x in weapons_to_nicknames.keys() if x not in weapons_df_names]
    logger.warning(f"Following guns redundant in nicknames dict, it should be updated! - {redundant_guns}")

"""
Generate categories for equipment
"""
df_equipment = pd.read_csv("./data/csgo_equipment.csv", sep=',')
# pre-generate the dictionary to manually fill the categories below
# equipment_to_categories = {x: 'something' for x in df_equipment['name'].tolist()}
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

equipment_to_nicknames = {
    'Kevlar Vest': 'kevlar',
    'Kevlar Vest + Helmet': 'kevlarhelmet',
    'Zeus x27': 'zeus',
    'Defuse Kit': 'defuse',
    'Molotov': 'molotovgrenade',
    'Incendiary Grenade': 'incendiarygrenade',
    'Decoy Grenade': 'decoygrenade',
    'Flashbang': 'flashbang',
    'HE Grenade': 'hegrenade',
    'Smoke Grenade': 'smokegrenade'
}


equipment_df_names = df_equipment['name'].tolist()

# check that all equipment is covered
if not all([x in equipment_to_categories for x in equipment_df_names]):
    missing_equipment = [x for x in equipment_df_names if x not in equipment_to_categories]
    raise AttributeError(f"Following equipment not covered in categories dict, it needs to be updated! - {missing_equipment}")

# check that all equipment is covered
if not all([x in equipment_to_nicknames for x in equipment_df_names]):
    missing_equipment = [x for x in equipment_df_names if x not in equipment_to_nicknames]
    raise AttributeError(f"Following equipment not covered in nicknames dict, it needs to be updated! - {missing_equipment}")

# check for equipment redundancy
if not all([x in equipment_df_names for x in equipment_to_categories.keys()]):
    redundant_equipment = [x for x in equipment_to_categories.keys() if x not in equipment_df_names]
    logger.warning(f"Following equipment redundant in categories dict, it should be updated! - {redundant_equipment}")

# check for equipment redundancy
if not all([x in equipment_df_names for x in equipment_to_nicknames.keys()]):
    redundant_equipment = [x for x in equipment_to_nicknames.keys() if x not in equipment_df_names]
    logger.warning(f"Following equipment redundant in nicknames dict, it should be updated! - {redundant_equipment}")


# merge dicts, create a df from them, save as csv
buyable_categories = weapons_to_categories | equipment_to_categories
buyable_nicknames = weapons_to_nicknames | equipment_to_nicknames
byuable_categories_df = pd.DataFrame({'name': list(buyable_categories.keys()),
                                      'category': list(buyable_categories.values()),
                                      'nickname': list(buyable_nicknames.values())
                                      })
byuable_categories_df.to_csv("./data/csgo_byuable_to_category_nickname.csv", index=False)
