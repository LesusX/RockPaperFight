'''
# Check if list is empty or not 
lista = [2]
if not lista:
    print("list is empty")
    print(lista) 
elif lista:
    print("List is not empty")
    print(lista)
''' 



class Champion:
    def __init__(self, name) -> None:
        self.health = 100 
        self.stamina = 100 
        self.name = name  


class FireChampion(Champion):
    def __init__(self, name) -> None:
        super().__init__(name)
        

myList = ["r","1","c","e","f","g"]
# i = 0
for i in myList[:]:
    if i != myList[0]:
        myList.remove(i)

print(myList)
