import json

def getIngredients(ingredient):
    with open('ingredients.json') as json_file:
        data = json.load(json_file)
        ingCaps = ingredient.upper()
        ingrData = data[ingCaps]
        return  ingrData


print(getIngredients("BARLEY, RAW"))