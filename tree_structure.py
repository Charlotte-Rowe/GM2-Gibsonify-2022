from anytree import Node, RenderTree, search

root = Node("Ingredient")
plant = Node("Plant based", parent=root)
animal = Node("Animal based", parent=root)
meat = Node("Meat", parent=animal)
fish = Node("Fish", parent=animal)
animalOther = Node("Other", parent=animal)
redMeat = Node("Red meat", parent=meat)
poultry = Node("Poultry", parent=meat)
beef = Node("Beef", parent=redMeat)
sheep = Node("Sheep", parent=redMeat)
goat = Node("Goat", parent=redMeat)
lamb = Node("Lamb", parent=sheep)
mutton = Node("Mutton", parent=sheep)
chickenMeat = Node("Chicken", parent=poultry)
turkey = Node("Turkey", parent=poultry)
duck = Node("Duck", parent=poultry)
chicken = Node("Chicken", parent=chickenMeat)
fowl = Node("Fowl", parent=chickenMeatchick)
dairy = Node("Dairy", parent=animalOther)
milk = Node("Milk", parent=dairy)
cheese = Node("Cheese", parent=dairy)
egg = Node("Egg", parent=animalOther)
chickEgg = Node("Chicken egg", parent=egg)
finfish = Node("Finfish", parent=fish)
shellfish = Node("Shellfish", parent=fish)
otherFish = Node("Other fish", parent=fish)

for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))


def findNearest(node):  # returns child above given node, on same level, which is assumed to be most similar
    siblings = node.parent.children
    closest = 0
    if len(siblings)>1: # ie the node input has siblings
        for i in(0, len(siblings)-1):
            if siblings[i]==node:
               closest = divmod((i-1), len(siblings))[1]
        return siblings[closest]

    if len(siblings) <= 1: # ie the node input does not have siblings
        parent = node.parent
        closest = findNearest(parent)
        if len(closest.children) !=0:
            return closest.children[0]
        return closest

print(findNearest(chicken).name)