import pandas as pd
import os
here = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(here, 'Appendix-1-D1_D2_D3_Sample Data.xlsx')
# Load the xlsx file
adult_file = pd.read_excel(filename, sheet_name = 1)
child_file = pd.read_excel(filename, sheet_name = 2)
# Read the values of the file in the dataframe
adult_data = pd.DataFrame(adult_file)
child_data = pd.DataFrame(child_file)
data = adult_data.merge(child_data, how='outer')

filename = os.path.join(here, 'Nutrient_names.txt')
with open(filename,'r') as data_file:
    nutrient_names = []
    for line in data_file:
        nutrient_names.append(line.split()[0])


# Gets Member IDs
mem_ID = data['MEM_ID']
members = []
for ID in mem_ID:
    if ID not in members:
        members.append(ID)
#print(members)
# Creates a list of tuples for a given member

rows = len(data.index)

def add_ret_factors():
    for nutrient in nutrient_names:
        ret_factors = []
        for i in range(rows):
            ret_factors.append(get_ret_factor(data.ITEM_OR_NAME_DISH[i], data.WHEN_EATEN[i], nutrient))
        print(nutrient)
        data['RET_'+ nutrient] = ret_factors

#def get_nutrient_info():

def get_ret_factor(food_name, cooking_method, nutrient_name):
    return 1

add_ret_factors()

print("The content of the file is:\n", data)
print(data.columns)