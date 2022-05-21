import pandas as pd
import os
here = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(here, 'Sample_Data.xlsx')
# Load the xlsx file
adult_file = pd.read_excel(filename, sheet_name = 1)
child_file = pd.read_excel(filename, sheet_name = 2)
# Read the values of the file in the dataframe
adult_data = pd.DataFrame(adult_file)
child_data = pd.DataFrame(child_file)
data = adult_data.merge(child_data, how='outer')
# Print the content
#print("The content of the file is:\n", data)
#print(data.columns)

# Gets Member IDs
mem_ID = data['MEM_ID']
members = []
for ID in mem_ID:
    if ID not in members:
        members.append(ID)
#print(members)
# Creates a list of tuples for a given member

rows = len(data.index)
food_list = []
for member in members:
    member_food = []
    row = 0
    for i in range(rows):
        if data.MEM_ID[i] == member:
            food_name = data.ITEM_OR_NAME_DISH[i]
            food_amount = data.MEASUREMENT[i]
            cooking_method = int(data.WHEN_EATEN[i])
            food_entry = (food_name, food_amount, cooking_method)
            member_food.append(food_entry)
    food_list.append(member_food)

mem_to_food = dict(zip(members, food_list))