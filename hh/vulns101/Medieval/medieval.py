# get this code to print "you win!"
# good luck :)

MEDIEVAL_THINGS = [
    "Knights",
    "Trebuchet",
    "Sword Fights",
    "Peasants",
    "Catapult",
    "Dragons"
]

if __name__ == '__main__':
    print("Here is a list of medieval items (things from the middle ages):")

    for i, thing in enumerate(MEDIEVAL_THINGS):
        print(f"{i + 1}. {thing}")

    option = input("Which one is your favorite (choose it's number)? ")
    favorite_index = eval(option) - 1

    print(f"Your favorite is {MEDIEVAL_THINGS[favorite_index]}!")
