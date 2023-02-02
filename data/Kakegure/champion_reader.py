from riotwatcher import LolWatcher, ApiError
import pandas as pd
import numpy as num
import csv

<<<<<<< HEAD
api_key = 'RGAPI-32db3421-d517-41c2-ba50-c22542d4cb0f'
=======
api_key = 'RGAPI-c273c4c5-5dcc-4319-bbb8-3161ab685d0c'
>>>>>>> 9a93e81984d4f15585042d3235d8cca82f8c96fc
watcher = LolWatcher(api_key)
my_region = 'na1'
version = "13.1.1"

# We use Data Dragon to pull Champion Data into a dictionary
champ_data = watcher.data_dragon.champions(version)

# Variable for getting Champion List -> cl
cl = champ_data.get('data')

# Traversing the dictionary to retrieve Champion Name
# and ID
data = []
champ_name = []
for x in cl:
    row = {}
    # Creating a local variable for data dictionary - Local List - LL
    LL = cl[x]
    nKey = LL.get('key')
    # Search dictionary for Key and save it
    for i in LL:
        if i == 'key':
            row['Champion'] = x
            row['ID'] = LL[i]
            data.append(row)
            champ_name.append(x)

# Data Frame / Table of Champ per ID
<<<<<<< HEAD
Champ_Frame = pd.DataFrame(data)
=======
Champ_Frame = pd.DataFrame(data)
>>>>>>> 9a93e81984d4f15585042d3235d8cca82f8c96fc
