str = "?X je rodic ?Y,manzelia ?X ?Z"

list_of_var = []

for i in range(len(str)):

    if str[i] == "?":

        if str[i + 1] not in list_of_var:
            list_of_var.append(str[i + 1])

slovo = "clovek"
var = [character.replace("c"," ") for character in slovo]
print(var)
print(list_of_var)
