import random


tick = 1
shelters = []
petName = 0

class counter(dict):
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)


class AnimalShelter:
    def __init__(self, name, capacity, pos, adoptRate):
        self.capacity = capacity
        self.pets = []
        self.name = str(name)
        self.adoptRate = adoptRate
        self.qVals = counter()
        self.alpha = .5
        self.pos = pos
        self.epsilon = 0.1

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

        return actions

    def computeActionFromQVals(self, state):
        maxQ = -999999.9
        retAction = None
        for action in self.getPossibleActions():
            test = self.getQValue(state, action)
            if(maxQ < test):
                maxQ = test
                retAction = action

        return retAction

    def getReward(self, action):
        #print(action)
        reward = 0.0
        if(action == "Nothing"):
            return reward
        shelter, pet = self.unpackAction(action)
        if(shelter != None and pet != None):
            #print("Shelter not none")
            if(shelter != self):
                reward += manhattanDistance(self.pos, shelter.pos)
            reward += pet.adoptRate / shelter.adoptRate

        #print(reward)
        return reward


    def getQValue(self, state, action):
        return self.qVals[(state, action)]

    def getPet(self, name):
        for p in self.pets:
            if p.name == name:
                return p
        return None

    # def updateQValsInitial(self, state, action):
    #     self.qVals.update({(state, action): (1 - self.alpha) * self.getQValue(state, action) + self.alpha * (self.getReward(action) + self.getQValue(state, action))})

    def updateQVals(self, state, action):
        nextState = self.nextStateFinder(state, action)
        nextAction = self.computeActionFromQVals(nextState)
        # print("NextAction: " + nextAction)
        self.qVals.update({(state, action): (1 - self.alpha) * self.getQValue(state, action) + self.alpha * (self.getReward(nextAction) + self.getQValue(nextState, nextAction))})
        #print("Updated "+ str(action) + ": " + str(self.qVals[action]))

    def performAction(self, action):
        if (action != "Nothing"):
            print("Not Nothing")
            shelter, pet  = self.unpackAction(action)
            if(shelter != None and pet != None):
                print("not none")
                if(shelter != self and pet in self.pets):
                    print("Moving")
                    shelter.insert(pet)
                    self.remove(pet)

    def flipCoin(self, p):
        r = random.random()
        return r < p

    def getAction(self, state):
        legalActions = self.getPossibleActions()
        if(self.flipCoin(self.epsilon)):
            return random.choice(legalActions)
        else:
            return self.computeActionFromQVals(state)

    def nextStateFinder(self, state, action):
        if (action != "Nothing"):
            shelter, pet = self.unpackAction(action)
            nextState = []
            if (shelter != self and pet in self.pets):
                shelter.insert(pet)
                self.remove(pet)
            for s in shelters:
                for p in s.pets:
                    nextState.append((s.name, p.name))
            if (shelter != self and pet in shelter.pets):
                shelter.remove(pet)
                self.insert(pet)
            nextState = tuple(nextState)
            return nextState
        else:
            return state

    def unpackAction(self, action):
        if (action != "Nothing"):
            return shelters[int(action[0])], self.getPet(str(action[3]))
        else:
            return None, None

class Pet:
    def __init__(self, tick, name, adoptRate):
        self.creationTick = tick
        self.name = str(name)
        self.adoptRate = adoptRate

def manhattanDistance(pos1, pos2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

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


def update(state):
    global petName

    for s in shelters:
        # print("In shelter: " + str(s.name) + ". Pets: " + str(s.pets) + ". Pos: " + str(s.pos))
        # print("Performing Q-Learn.")
        for action in s.getPossibleActions():
            s.updateQVals(state, action)
        # print("Q-Learn Complete. Choosing Action")
        action = s.getAction(state)
        print("Action picked: " + str(action))
        s.performAction(action)
        # print("Action performed")


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
    petIndex = 0


    # f = open("shelters.txt")
    # line = f.readline()
    # index = 1
    #
    # while(line):
    #     shelters.append(AnimalShelter(str(index), int(line)))
    #     line = f.readline()
    #     index +=1

    shelters.append(AnimalShelter(str(0), 5, (0, 0), 0.5))
    shelters.append(AnimalShelter(str(1), 4, (1, 2), 0.2))
    shelters.append(AnimalShelter(str(2), 2, (4, 8), 0.8))

    shelters[0].insert(Pet(tick, str(1), random.randrange(20, 70)*.01))
    shelters[0].insert(Pet(tick, str(2), random.randrange(20, 70)*.01))
    shelters[0].insert(Pet(tick, str(3), random.randrange(20, 70)*.01))
    shelters[1].insert(Pet(tick, str(4), random.randrange(20, 70)*.01))
    shelters[1].insert(Pet(tick, str(5), random.randrange(20, 70)*.01))
    shelters[2].insert(Pet(tick, str(6), random.randrange(20, 70)*.01))
    shelters[2].insert(Pet(tick, str(7), random.randrange(20, 70)*.01))

    petIndex = 8
    state = []
    for s in shelters:
        for p in s.pets:
            state.append((s.name, p.name))

    state = tuple(state)
    print(type(state))

    for s in shelters:
        for action in s.getPossibleActions():
            s.updateQVals(state, action)


    f = open("data.txt")
    line = f.readline()
    while(line):
        state = []
        newPet = None
        newPetRate = int(line) * .01
        if(newPetRate != 0.0 ):
            newPet = Pet(tick, str(petIndex), newPetRate)
            petIndex += 1
            s = findShelter()
            s.insert(newPet)
        print("************************")
        print("Tick: " + str(tick))
        if(newPet != None ):
            print("New Pet: " + newPet.name + " " + str(newPet.adoptRate))
        for s in shelters:
            print("Shelter " + str(s.name) + " (" + str(s.adoptRate) + "): ")
            for p in s.pets:
                print(p.name+ " " + str(p.adoptRate))
            print("Pos: " + str(s.pos))
        print("************************")
        for s in shelters:
            for p in s.pets:
                state.append((s.name, p.name))
        state = tuple(state)
        update(state)
        line = f.readline()
        tick +=1

main()