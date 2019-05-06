import random


tick = 1
shelters = []
petName = 0

class counter(dict):
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)


class AnimalShelter:
    def __init__(self, name, capacity, pos):
        self.capacity = capacity
        self.pets = []
        self.name = str(name)
        self.adoptionRate = .5
        self.qVals = counter()
        self.alpha = .5
        self.pos = pos
        self.epsilon = 0.5

    def insert(self, pet):
        if(not self.isFull()):
            self.pets.append(pet)

    def remove(self, pet):
        if(not self.isEmpty()):
            self.pets.remove(pet)

    def size(self):
        return len(self.pets)

    def isFull(self):
        return self.size() == self.capacity

    def isEmpty(self):
        return self.size() == 0

    def getPossibleActions(self):
        "2: 3"
        actions = []
        actions.append("Nothing")
        for s in shelters:
            if(s.name == self.name):
                continue
            if(not s.isFull()):
                for p in self.pets:
                    actions.append(str(s.name) + ": " + str(p.name))

        for p in self.pets:
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
        reward = 0.0
        shelter, pet = self.unpackAction(action)
        if(shelter != None):
            #print("Shelter not none")
            if(shelter != self):
                reward = self.manhattanDistance(self.pos, shelter.pos)

        print(reward)
        return reward


    def getQValue(self, action):
        return self.qVals[action]

    def getPet(self, name):
        for p in self.pets:
            if p.name == name:
                return p
        return None

    def unpackAction(self, action):
        if(action != "Nothing"):
            return shelters[int(action[0])], self.getPet(str(action[3]))
        else:
            return None, None

    def manhattanDistance(self, pos1, pos2):
        "Returns the Manhattan distance between points xy1 and xy2"
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def updateQValsInitial(self, action):
        self.qVals.update({action: (1 - self.alpha) * self.getQValue(action) + self.alpha * (self.getReward(action) + self.getQValue(action))})

    def updateQVals(self, action):
        nextAction = self.computeActionFromQVals()
        print("NextAction: " + nextAction)
        self.qVals.update({action: (1 - self.alpha) * self.getQValue(action) + self.alpha * (self.getReward(nextAction) + self.getQValue(nextAction))})

    def performAction(self, action):
        shelter, pet  = self.unpackAction(action)
        if(shelter != None and pet != None):
            if(shelter != self):
                shelter.insert(pet)
                self.remove(pet)

    def flipCoin(self, p):
        r = random.random()
        return r < p

    def getAction(self):
        legalActions = self.getPossibleActions()
        if(self.flipCoin(self.epsilon)):
            return random.choice(legalActions)
        else:
            return self.computeActionFromQVals()

class Pet:
    def __init__(self, tick, name):
        self.creationTick = tick
        self.name = str(name)



def findShelter():
    for s in shelters:
        if(not s.isFull()):
            return s
    return None

# def update(petCount):
#     global petName
#
#     #updateQVals()
#
#
#     for i in range(petCount):
#         p = Pet(tick, str(petName))
#         petName += 1
#         s = findShelter()
#         try:
#             s.insert(p)
#             print("Inserted pet into shelter " + s.name)
#         except AttributeError:
#             print("No available shelter found.")
#
#
# def main():
#     global tick
#
#
#     f = open("shelters.txt")
#     line = f.readline()
#     index = 1
#
#     while(line):
#         shelters.append(AnimalShelter(str(index), int(line)))
#         line = f.readline()
#         index +=1
#
#
#     f = open("data.txt")
#     line = f.readline()
#     while(line):
#         print("Tick: " + str(tick))
#         update(int(line))
#         line = f.readline()
#         tick +=1


def update(petCount):
    global petName

    for s in shelters:
        print("In shelter: " + str(s.name) + ". Pets: " + str(s.pets) + ". Pos: " + str(s.pos))
        print("Performing Q-Learn.")
        for action in s.getPossibleActions():
            s.updateQVals(action)
        print("Q-Learn Complete. Choosing Action")
        action = s.getAction()
        print("Action picked: " + str(action))
        s.performAction(action)
        print("Action performed")


    # for i in range(petCount):
    #     p = Pet(tick, str(petName))
    #     petName += 1
    #     s = findShelter()
    #     try:
    #         s.insert(p)
    #         print("Inserted pet into shelter " + s.name)
    #     except AttributeError:
    #         print("No available shelter found.")


def main():
    global tick


    # f = open("shelters.txt")
    # line = f.readline()
    # index = 1
    #
    # while(line):
    #     shelters.append(AnimalShelter(str(index), int(line)))
    #     line = f.readline()
    #     index +=1

    shelters.append(AnimalShelter(str(0), 5, (0, 0)))
    shelters.append(AnimalShelter(str(1), 4, (1, 2)))
    shelters.append(AnimalShelter(str(2), 2, (4, 8)))

    shelters[0].insert(Pet(tick, str(1)))
    shelters[0].insert(Pet(tick, str(2)))
    shelters[0].insert(Pet(tick, str(3)))
    shelters[1].insert(Pet(tick, str(4)))
    shelters[1].insert(Pet(tick, str(5)))
    shelters[2].insert(Pet(tick, str(6)))
    shelters[2].insert(Pet(tick, str(7)))

    for s in shelters:
        for action in s.getPossibleActions():
            s.updateQValsInitial(action)


    f = open("data.txt")
    line = f.readline()
    while(line):
        print("Tick: " + str(tick))
        for s in shelters:
            print("Shelter " + str(s.name) + ". Pets: " + str(s.pets) + ". Pos: " + str(s.pos))
        update(int(line))
        line = f.readline()
        tick +=1

main()