from queue import Empty
import pandas as pd
import os
here = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(here, 'Type_to_Retention.csv')
type_retention = pd.read_csv(filename)
retention_data = pd.DataFrame(type_retention)

filename = os.path.join(here, 'name_method_num_to_method_type.xlsx')
type_retention = pd.read_excel(filename)
method_table = pd.DataFrame(type_retention)

filename = os.path.join(here, 'new_data!.xlsx')
sample_dataset = pd.read_excel(filename)
data = pd.DataFrame(sample_dataset)


#print("The content of the file is:\n", data)

# Desc list built with list format: Food type, Additional info...

def build_desc_list():
    food_types = retention_data['R_Descr']
    types = []
    for description in food_types:
        type =  description.split(',')
        if type not in types:
            types.append(type)
    return types

# Best Guess of Food Type from input description (need in format: type, additional info 1,...) - should now be redundant

def best_type_guess(descr):
    poss_desc_list = []
    type = descr[0]
    for desc in desc_list:
        if desc[0] == type:
            poss_desc_list.append(desc)
    if poss_desc_list is Empty:
        print('No valid Description for ' + str(descr))

    max_points = 0
    best_guess_list = []
    for desc in poss_desc_list:
        points = 0
        for item in descr: # Ranking algorithm needs refinement
            if item in desc:
                points += 1
        if points > max_points:
            best_guess_list = []
            best_guess_list.append(desc)
            max_points = points
        elif points == max_points:
            best_guess_list.append(desc)
    if len(best_guess_list) == 1:
        return best_guess_list[0]
    else:
        for guess in best_guess_list:
            print(guess)
        best_guess = input('Select best description of ' + str(descr) + ' from list above (Select 1 for first option, 2 for second, ...) ')
        return best_guess_list[int(best_guess) - 1]

# Fetches Retention Factors provided description is in appropriate format

def fetch_ret_factors(entry):
    ret_list = retention_data.columns.values[2:]
    row_val = desc_list.index(entry)
    levels = retention_data.loc[row_val][2:]
    #ret_levels = dict(zip(ret_list, levels))
    return levels

# Build dictionary relating cooking method numbers to cooking methods - now REDUNDANT

def build_cooking_method_list():
    method_codes = []
    method = []
    codes = list(data['Code'])
    descriptions = list(data['Description'])
    list_start_index = data.index[data['Varuiable'] == 'WHEN_EATEN'].values[0]
    list_end_index = data.index[data['Varuiable'] == 'MEASUR_METHOD'].values[0]
    index = list_start_index
    while index < list_end_index:
        method_codes.append(codes[index])
        method.append(descriptions[index].upper())
        index += 1
    code_to_method = dict(zip(method_codes, method))
    return code_to_method

# Fetch best guess of cooking method from method number and food type

def fetch_cooking_method(food_type, method_number):
    methods = method_table[food_type]
    return methods[method_number - 1]

desc_list=build_desc_list()

#ret_cheese_baked = fetch_ret_factors(['CHEESE', 'BAKED'])
#print(ret_cheese_baked)
#method_list = build_cooking_method_list()
#print(method_list[2])
#c_method = fetch_cooking_method('CHEESE',1)
#print(c_method)