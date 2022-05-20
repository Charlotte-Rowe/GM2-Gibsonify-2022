import json


def getIngredients(ingredient):
    # gets nutrient information
    # ingredient must match ingredient name in all ways except the case
    with open('ingredients.json') as json_file:
        data = json.load(json_file)
        ingCaps = ingredient.upper()
        ingrData = data[ingCaps]
        return ingrData


print(getIngredients("BARLEY, RAW"))


def getIngredientsRelevant(ingredient):
    # ingredient must contain words in the target ingredient object, returns possible objects
    with open('ingredients.json') as json_file:
        data = json.load(json_file)
        ingCaps = ingredient.upper()
        words = ingCaps.split()
        print(words)
        possible = []
        for item in data:
            for word in range(0, len(words)):
                if item.find(words[word]) != -1:
                    possible.append(item)
        return possible


print(getIngredientsRelevant("ONION"))

def getIngredientGroup(ingredient):
    # gets group from exact ingredient name
    with open('groups.json') as json_file:
        data = json.load(json_file)
        details = data[ingredient]
        group = details['G_Descr']
        return(group)


print(getIngredientGroup("BARLEY, RAW"))

