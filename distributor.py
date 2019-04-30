
tick = 1
shelters = []
petName = 0

class counter(dict):
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)


class AnimalShelter:
    def __init__(self, name, capacity):
        self.capacity = capacity
        self.pets = []
        self.name = str(name)
        self.adoptionRate = .5
        self.qVals = counter()
        self.alpha = .5

    def insert(self, pet):
        if(not self.isFull()):
            self.pets.append(pet)

    def size(self):
        return len(self.pets)

    def isFull(self):
        return self.size() == self.capacity

    def getPossibleActions(self):
        "2: 3"
        actions = []
        actions.append("Nothing")
        for s in shelters:
            if(s.name == self.name):
                continue
            for p in self.pets:
                actions.append(str(s.name) + ": " + str(p.name))
                actions.append("0: " + str(p.name))

        return actions

    def computeActionFromQVals(self):
        maxQ = -999999.9
        retAction = None
        for action in self.getPossibleActions():
            test = self.getQValue(action)
            if(maxQ < test):
                maxQ = test
                retAction = action

        return retAction

    def getReward(self, action):
        return 1

    def getQValue(self, action):
        return self.qVals[action]

    def updateQVals(self, action):
        nextAction = self.computeActionFromQVals()
        self.qVals.update({action: (1 - self.alpha) * self.getQValue(action) + self.alpha * (self.getReward(nextAction) + self.getQValue(nextAction))})

class Pet:
    def __init__(self, tick, name):
        self.creationTick = tick
        self.name = str(name)



def findShelter():
    for s in shelters:
        if(not s.isFull()):
            return s
    return None

def update(petCount):
    global petName

    #updateQVals()


    for i in range(petCount):
        p = Pet(tick, str(petName))
        petName += 1
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