class Person:
    species = "Human" # class attribute
    
    def __init__(self, name):
        self.name = name
        self.species = "Alien" #instance attribute shadows the class attribute
        
p1 = Person("John")
print("Instance species: ", p1.species)
print("Class species: ", Person.species)
      

