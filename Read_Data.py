import pandas as pd
import os
import getRetentionFactors as grf
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(here, 'new_data!.xlsx')
file = pd.read_excel(filename)
data = pd.DataFrame(file)

filename = os.path.join(here, 'Type_to_Retention.csv')
type_retention = pd.read_csv(filename)
retention_data = pd.DataFrame(type_retention)

filename = os.path.join(here, 'name_method_num_to_method_type.xlsx')
type_retention = pd.read_excel(filename)
method_table = pd.DataFrame(type_retention)

filename = os.path.join(here, 'Nutrient_names.txt')
with open(filename,'r') as data_file:
    nutrient_names = []
    for line in data_file:
        nutrient_names.append(line.split()[0])

rows = len(data.index)

# Gets Member IDs

def fetch_members():
    mem_ID = data['MEM_ID']
    members = []
    for ID in mem_ID:
        if ID not in members:
            members.append(ID)
    return members

# Adds columns to data table detailing retention factors for each nutrient

def add_ret_factors():
    for nutrient in nutrient_names:
        for i in range(rows):
            data['RET_'+ nutrient] = 1
    for i in range(rows):
        ret_factors=get_ret_factor(data.INGREDIENT_NAME[i], data.WHEN_EATEN[i])
        for j in range(len(nutrient_names)):
            data['RET_'+ nutrient_names[j]].iloc[i] = ret_factors[j]

# Adds columns to data table detailing nutrient values for each nutrient - needs to be completed

def add_nutrient_info():
    for nutrient in nutrient_names:
        for i in range(rows):
            data[nutrient] = 1
    for i in range(rows):
        nutrient_info=get_nutrient_info(data.INGREDIENT_NAME[i], data.WHEN_EATEN[i], data.WEIGHT_IN_G[i])
        for j in range(len(nutrient_names)):
            data[nutrient_names[j]].iloc[i] = nutrient_info[j]

# Fetches retention factors from either table

def get_ret_factor(food_name, cooking_method):
    if check_nutrient_table(food_name, cooking_method) == 1:
        food_type = get_food_type(food_name)
        method = grf.fetch_cooking_method(food_type, cooking_method)
        if method == 'FULL_RETENTION':
            return np.ones(26)
        else:
            return grf.fetch_ret_factors([food_type, method])
    else:
        return check_nutrient_table(food_name, cooking_method)

# Gets nutritional information from nutrient tables - needs to be completed

def get_nutrient_info(food_name, cooking_method, nutrient_name, mass):
    return 1

# Checks if nutrient entry includes retention info already - needs to be completed

def check_nutrient_table(food_name, cooking_method):
    return 1

# Fetches food type - needs to be completed

def get_food_type (food_name):
    return 'VEG(GREENS)'

add_ret_factors()
#add_nutrient_info()

print("The content of the file is:\n", data)