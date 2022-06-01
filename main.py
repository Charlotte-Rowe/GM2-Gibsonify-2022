from re import M
import pandas as pd
import os
import getRetentionFactors as grf
import getIngredientDetails as gid
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

filename = os.path.join(here, 'Appendix-1-D1_D2_D3_Sample Data.xlsx')
file = pd.read_excel(filename)
all_codes = pd.DataFrame(file)

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



missed = []

# Adds columns to data table detailing nutrient values for each nutrient
def add_nutrient_info():
    for nutrient in nutrient_names:
        for i in range(rows):
            data[nutrient] = 1
    for i in range(rows):
        nutrient_info=get_nutrient_info(data.INGREDIENT_NAME[i], data.WHEN_EATEN[i], data.WEIGHT_IN_G[i])
        if nutrient_info == 0:
            if data.INGREDIENT_NAME[i] not in missed:
                print("no ingredient: ",data.INGREDIENT_NAME[i])
                missed.append(data.INGREDIENT_NAME[i])
            nutrient_info = np.zeros(26)
        for j in range(len(nutrient_names)):
            data[nutrient_names[j]].iloc[i] = nutrient_info[j]


# Fetches retention factors from either table
def get_ret_factor(food_name, cooking_method):
    c_method_list = grf.build_cooking_method_list()
    c_method = c_method_list[cooking_method]
    if check_nutrient_table(food_name, c_method) == 0:  # = 0 if no info in nutrient table
        food_type = get_food_type(food_name)    # will return 0 if not possible/no retention group for that food, -1 if food name doesn't match
        if type(food_type) == int:
            return np.ones(26)
        else:
            method = grf.fetch_cooking_method(food_type, cooking_method)
            if method == 'FULL_RETENTION':
                return np.ones(26)
            else:
                b_guess = grf.best_type_guess([food_type, method])
                return grf.fetch_ret_factors(b_guess)
    else:
        return np.ones(26)


# Gets nutritional information from nutrient tables
def get_nutrient_info(food_name, cooking_method, mass):
    ingredient = ""
    c_method_list = grf.build_cooking_method_list()
    c_method = c_method_list[cooking_method]
    if gid.cookingMethodEntry(food_name, c_method) != 0:
        ingredient = gid.cookingMethodEntry(food_name, c_method)[0]
    else:
        ingredient = gid.getIngredientsRelevant(food_name)
        if len(ingredient) == 0:
            return 0
        ingredient = ingredient[0]
    nutrients = gid.getIngredients(ingredient)
    nutrients = nutrients.values.tolist()
    nutrients = nutrients[2:]
    temp = nutrients[15]
    nutrients[15] = nutrients[17]
    nutrients[17] = temp
    return nutrients


# get_nutrient_info("potato", "boiled", 100)

# Checks if nutrient entry includes retention info already
def check_nutrient_table(food_name, cooking_method):
    if gid.cookingMethodEntry(food_name, cooking_method) != 0:
        return 1
    return 0


missing = []


# Fetches food type
def get_food_type (food_name):
    ingredient = gid.getIngredientsRelevant(food_name)
    food_entry = ""
    if len(ingredient) >= 1:
        food_entry = ingredient[0]  # so no manual entry is needed just take the first possible food
        group = gid.matchGroups(food_entry)
        if group == 0:
            return 0    # no retention group for this ingredient
        return group
    else:
        if food_name not in missing:
            print("Get food type error: no ingredient found matching ",food_name)
            missing.append(food_name)
        return -1    # no ingredients matching food name

# Creates output in form: member_ID, total nutrient 1, total nutrient 2, ...

def create_output():
    member_list = fetch_members()
    members = {'MEMBERS': member_list}
    no_members=len(member_list)
    output_data = pd.DataFrame(members)
    for nutrient in nutrient_names:
        nutrient_for_member = np.zeros(no_members)
        for i in range(rows):
            ret_factor = data['RET_'+ nutrient].iloc[i]
            nut_level = data[nutrient].iloc[i]
            member = data['MEM_ID'].iloc[i]
            print(member)
            index = member_list.index(member)
            nutrient_for_member[index] += nut_level * ret_factor
        output_data[nutrient] = nutrient_for_member
    return(output_data)

add_nutrient_info()
add_ret_factors()

filename = os.path.join(here, 'Output.xlsx')
file = pd.read_excel(filename)
data = pd.DataFrame(file)


output_data = create_output()

#print("The content of the file is:\n", output_data)

filename = os.path.join(here, 'Output2.xlsx')
output_data.to_excel(filename, index=False)
