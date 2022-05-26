from math import nan
import numpy as np
import pandas as pd
import os


df = pd.read_excel('sample.xlsx')
raw_data = pd.DataFrame(df)
df1 = pd.read_excel('recipe_sample.xlsx')
recipe_data = pd.DataFrame(df1)

new_data = raw_data
new_data['weight in g'] = 0
#Now the adult data in new_data and ingredient data in raw data
print(recipe_data)

#divide recipe into find_volume and find_mass, the former is for things like curry, the latter is for things like apple
find_mass=[]
find_volume=[]

for i in range(len(recipe_data)):
    a = recipe_data['RECIPE_QTY'][i]
    if type(a) == str:
        b= recipe_data['RECIPE_NO'][i]
        if b not in find_mass:
            find_mass.append(b)
    else:
        c= recipe_data['RECIPE_NO'][i]
        if c not in find_volume:
            find_volume.append(c)
print(find_volume)
print(find_mass)