import json
import pandas

def getIngredients(ingredient):
    # gets nutrient information
    # ingredient must match ingredient name in all ways except the case
    data = pandas.read_json('ingredients.json')
    caps = ingredient.upper()
    ingData = data[caps]
    return ingData


#print(getIngredients("BARLEY, RAW"))


def getIngredientsRelevant(ingredient):
    # ingredient must contain words in the target ingredient object, returns possible objects
    data = pandas.read_json('ingredients.json')
    ingCaps = ingredient.upper()
    words = ingCaps.split()
    #print(words)
    possible = []
    for item in data:
        for word in range(0, len(words)):
            if item.find(words[word]) != -1:
                possible.append(item)
    return possible


#print(getIngredientsRelevant("ONION"))


def getIngredientGroup(ingredient):
    # gets group from exact ingredient name
    data = pandas.read_json('groups_updated.json')
    details = data[ingredient]
    group = details['G_Descr']
    return group


#print(getIngredientGroup("BARLEY, RAW"))


def hasCookingMethod(ingredient):
    # return true if contains cooking method in ingredient name
    # assume the ingredient name is exact
    methods = ['BOILED', 'ROASTED', 'FRIED'] # this needs to be checked
    for method in methods:
        if ingredient.find(method) != -1:
            return method
    return False


#print(hasCookingMethod('ONION SMALL BOILED'))

def matchGroups(ingredient):
    group = getIngredientGroup(ingredient)
    data = pandas.read_csv('group_conversion.csv')
    data = pandas.DataFrame(data)
    possible = []
    groups = data['Groups']
    retentionGroup = data['Retention']
    groupCode = data['Match']
    for i in range(0, len(groups)-1):
        if groups[i]==group:
            if groupCode[i] == 0: # there is only one matching group
                return retentionGroup[i]
            elif groupCode[i] == 2:
                return 0 # this means that there is no retention factor data for this ingredient
            possible.append(retentionGroup[i])
    contains = []
    for j in range(0, len(possible)):
        type = possible[j]
        if ingredient.find(type) != -1:
            contains.append(type)
    if len(contains) == 0:
        return possible[-1]
    elif len(contains)==1:
        return contains[0]
    return contains


def getDetails():
    ingredient = input("Enter ingredient name:  ")
    possible = getIngredientsRelevant(ingredient)
    if len(possible) == 0:
        return "ERROR: no ingredients match this name"
    elif len(possible) == 1:
        ingredient = possible[0]
    elif len(possible) > 1:
        print("Possible ingredients: ",possible)
        picked = False
        chosen = 0
        while picked == False:
            chosen = input("Please enter a number between 1 and "+str(len(possible))+":  ")
            if not chosen.isnumeric():
                print("INVALID INPUT: please enter a number \n")
            elif (int(chosen) >= 1) & (int(chosen) <= len(possible)):
                picked = True
            else:
                print("That is not an option.")
        ingredient = possible[int(chosen)-1]
    details = getIngredients(ingredient)
    group = matchGroups(ingredient)     # have made the default values pork, seafood, veg(root), cereal, veg oil, milk
    method = hasCookingMethod(ingredient)
    if method != 0:     # if method not = 0 then dont get retention factor
        group = 0 # if group = 0 we do not get the retention factor
    return [group, method, details]


#print(matchGroups("ONION SMALL BOILED"))
#print(matchGroups("BARLEY, RAW"))
print(getDetails())

