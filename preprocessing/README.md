# Preprocessing

This folder contains scripts that need to run in order to generate all the data that's necessary for running the scripts for main analysis. 
Following scripts need to be run in specified order:

1. **01_generate_buyable_categories.py** - this script will generate file with buyable name, nickname, and category. It is necessary for further processing
2. **preprocessing.py** - script to put information from all files together into one so it can be used
for data mining exercises. This needs to be run before main analysis.

Following file is also part of this folder. However, it is not necessary to run it, it
contains functions that preprocessing.py needs to run. These function were moved to a separate file
for easier organisation.

**preprocessing_functions.py** - script containing functions necessary to run preprocessing.py

