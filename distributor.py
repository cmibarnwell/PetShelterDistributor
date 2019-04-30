
tick = 1
shelters = []


class AnimalShelter:
    def __init__(self, name, capacity):
        self.capacity = capacity
        self.pets = []
        self.name = str(name)

    def insert(self, pet):
        if(not self.isFull()):
            self.pets.append(pet)

    def size(self):
        return len(self.pets)

    def isFull(self):
        return self.size() == self.capacity

class Pet:
    def __init__(self, tick):
        self.creationTick = tick



def findShelter():
    for s in shelters:
        if(not s.isFull()):
            return s
    return None

def update(petCount):
    for i in range(petCount):
        p = Pet(tick)
        s = findShelter()
        try:
            s.insert(p)
            print("Inserted pet into shelter " + s.name)
        except AttributeError:
            print("No available shelter found.")


def main():
    global tick


    f = open("shelters.txt")
    line = f.readline()
    index = 1

    while(line):
        shelters.append(AnimalShelter(str(index), int(line)))
        line = f.readline()
        index +=1


    f = open("data.txt")
    line = f.readline()
    while(line):
        print("Tick: " + str(tick))
        update(int(line))
        line = f.readline()
        tick +=1

main()