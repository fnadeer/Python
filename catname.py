catnames = []
while True:
    print("Enter the name of the cat" + str(len(catnames) + 1) +" (Or enter nothing to stop) :")
    name = input()
    if name == '':
        break
    catnames = catnames + [name] #list concatenation
print("The cat names are: ")
for name in catnames:
    print('' + name)
