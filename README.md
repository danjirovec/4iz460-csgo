# 4IZ460 CleverMiner Project
This project operates on data from datasets

https://www.kaggle.com/datasets/christianlillelund/csgo-round-winner-classification

https://www.kaggle.com/datasets/vatsalparsaniya/csgo-weapons

## Requirements
- Python v 3.10 (or higher)

To install necessary packages, run following command:

`pip install -r requirements.txt`

## Project structure
 * **helper_scripts** - scripts for generating extra data that weren't in original files
   (run this first)
 * **preprocessing** - scripts to process all datasets together (scripts in helper_scripts 
should be run first, this should be run second)
 * ~~**main.ipynb** - main analysis script (should be run last)~~
 * **01_4ft_price_to_result.py** - script containing first task exploring how equipment cost influences round result
 
