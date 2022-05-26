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
nutrient_names_file = open(filename, 'r')
nutrient_names = nutrient_names_file.read()
print(nutrient_names)


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
    ret_factors = []
    for i in range(rows):
        for nutrient in nutrient_names:
            ret_factors.append(get_ret_factor(data.ITEM_OR_NAME_DISH[i], data.WHEN_EATEN[i]))
    data=data.assign(RET_FACTORS = ret_factors)

#def get_nutrient_info():
