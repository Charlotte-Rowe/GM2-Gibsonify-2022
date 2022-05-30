from math import nan
import numpy as np
import pandas as pd
import os

df = pd.read_excel('sample.xlsx')
raw_data = pd.DataFrame(df)
df1 = pd.read_excel('recipe_sample.xlsx')
recipe_data = pd.DataFrame(df1)
new_data = raw_data

new_data['volume in ml'] = 0
new_data['SL_No'] = 1
new_data['ingredient_name'] = pd.NA
new_data['weight in g']=0
#Now the adult data in new_data and ingredient data in raw data
#print(recipe_data)
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



#Now find mass for the recipe in find_mass:
for i in range(len(raw_data)):
    a = new_data['RECIPE_NUMBER'][i]
    if a in find_mass:
        new_data.loc[i,'ingredient_name'] = new_data.loc[i,'ITEM_OR_NAME_DISH']
        new_data.loc[i,'weight in g'] = 'To be found'
        method=df['MEASUR_METHOD'][i]
        if method == 1:
            wei = float(new_data.loc[i,'MEASUREMENT'])
            new_data.loc[i,'weight in g'] = 1000*wei
        if method == 2:
            new_data.loc[i,'volume in ml'] = float(new_data.loc[i,'MEASUREMENT'])
            density = 1 #need modify!
            new_data.loc[i,'weight in g'] = new_data.loc[i,'volume in ml']*density
        if method == 3: #need modify
            if new_data.loc[i,'SIZE'] == 1:
                vol= 2
            if new_data.loc[i,'SIZE'] == 2:
                vol= 4
            if new_data.loc[i,'SIZE'] == 3:
                vol= 30
            if new_data.loc[i,'SIZE'] == 4:
                vol= 5
            if new_data.loc[i,'SIZE'] == 5:
                vol= 10
            if new_data.loc[i,'SIZE'] == 6:
                vol= 20
            if new_data.loc[i,'SIZE'] == 7:
                vol= 3
            new_data.loc[i,'volume in ml'] = float(new_data.loc[i,'MEASUREMENT'])*vol
            density = 1 #need modify!
            new_data.loc[i,'weight in g'] = new_data.loc[i,'volume in ml']*density
            #the above is just there to give some reasonable output, method 3 I haven't figure out 
        if method == 5:
            new_data.loc[i,'volume in ml'] = 10*float(new_data.loc[i,'MEASUREMENT'])
            density = 1 #need modify!
            new_data.loc[i,'weight in g'] = new_data.loc[i,'volume in ml']*density
            #the above is just there to give some reasonable output, method 5 I haven't figure out 
        if method == 6:
            new_data.loc[i,'volume in ml'] = 10*float(new_data.loc[i,'SIZE'])
            density = 1 #need modify!
            new_data.loc[i,'weight in g'] = new_data.loc[i,'volume in ml']*density
            #the above is just there to give some reasonable output, method 6 I haven't figure out




#Now find volume for the recipe in find_volume:
for i in range(len(raw_data)):
    a = new_data['RECIPE_NUMBER'][i]
    if a in find_volume:
        new_data.loc[i,'ingredient_name'] = 'To be found'
        new_data.loc[i,'volume in ml'] = 'To be found'
        method=df['MEASUR_METHOD'][i]
        if method == 2:
            new_data.loc[i,'volume in ml'] = float(new_data.loc[i,'MEASUREMENT'])
            density = 1 #need modify!
        if method == 3:
            if new_data.loc[i,'SIZE'] == 1:
                vol= 2
            if new_data.loc[i,'SIZE'] == 2:
                vol= 4
            if new_data.loc[i,'SIZE'] == 3:
                vol= 30
            if new_data.loc[i,'SIZE'] == 4:
                vol= 5
            if new_data.loc[i,'SIZE'] == 5:
                vol= 10
            if new_data.loc[i,'SIZE'] == 6:
                vol= 20
            if new_data.loc[i,'SIZE'] == 7:
                vol= 3
            new_data.loc[i,'volume in ml'] = float(new_data.loc[i,'MEASUREMENT'])*vol
        if method == 4:
            new_data.loc[i,'volume in ml'] = 1000*float(new_data.loc[i,'MEASUREMENT'])
            #need modify


#Now find mass for the ingredients of recipe in find_volume:
new_data_final=pd.DataFrame()
for i in range(len(raw_data)):
    a = new_data['RECIPE_NUMBER'][i]
    if a in find_mass:
        q = new_data.loc[i]
        p=pd.DataFrame(q).T
        new_data_final=new_data_final.append(p)
    if a in find_volume:
        count=0
        for k in range(len(recipe_data)):
            if recipe_data['RECIPE_NO'][k] == a:
                count = count+1
                
                q = new_data.loc[i]
                p=pd.DataFrame(q).T
                p['ingredient_name'] = recipe_data['INGREDIENT_NAME'][k]
                p['weight in g'] = 1000*float(recipe_data['WEIGHT_IN_KGS'][k])*float(new_data.loc[i,'volume in ml'])/float(recipe_data['RECIPE_QTY'][k])
                p['SL_No'] = count
                new_data_final=new_data_final.append(p)
new_data_final.drop(['MEASUR_METHOD','MEASUREMENT','GRAMS_OR_ML','SIZE','NUMBER','volume in ml'], axis=1)

        

writer = pd.ExcelWriter('new_data!.xlsx')
new_data_final.to_excel(writer)
writer.save()