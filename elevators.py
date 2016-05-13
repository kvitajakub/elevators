
class Elevator:

    def __init__(self):
        self.floor = 0
        self.goals = [ None ]
        self.direction = 0

    def status(self):
        # TODO return back
        # return [self.floor, self.goals[0]]
        return [self.floor] + [self.goals]

    def addGoal(self, goal):
        self.goals.insert(-1,goal)
        self.sortGoals()

    def sortGoals(self):
        '''
        Some sort of scheduling system for one elevator, probably trying to maximize movement in one direction.
        Remove redundancies, each floor only once.
        '''
        # TODO ADD SORTING ALGORITHM
        lowerGoals = []
        higherGoals = []
        #remove none and duplicates
        self.goals.remove(None)
        self.goals = list(set(self.goals))

        for goal in self.goals:
            if goal > self.floor:
                higherGoals.append(goal)
            elif goal < self.floor:
                lowerGoals.append(goal)

        higherGoals.sort()
        lowerGoals.sort()
        lowerGoals.reverse()

        if self.direction == 1:
            self.goals = higherGoals + lowerGoals
        else:
            self.goals = lowerGoals + higherGoals

        self.goals.append(None)

        if self.goals[0] != None:
            self.direction = -1 if self.floor > self.goals[0] else 1


    def step(self):
        '''
        Perform one step of simulation.
        '''
        if self.goals[0] != None:
            self.floor += self.direction
            if self.floor == self.goals[0]:
                self.goals.pop(0)
                if self.goals[0] != None:
                    self.direction = -1 if self.floor > self.goals[0] else 1
                else:
                    self.direction = 0

class ElevatorControlSystem:
    def __init__(self, elevators=4):
        self.elevators = []
        for i in range(elevators):
            self.elevators.append(Elevator())

    def status(self):
        data = []
        for i in range(len(self.elevators)):
            data.append([i] + self.elevators[i].status())
        return data

    def update(self, ID, floor=None, newGoal=None):
        '''
        How can update() change floor of the elevator? Physically imposible, but okay.
        Add the new goal to the elevator.
        '''
        if ID < 0 or ID >= len(self.elevators):
            raise Exception('No elevator with ID = ' + str(ID))
        else:
            if floor != None:
                self.elevators[ID].floor = floor
            if newGoal != None:
                self.elevators[ID].addGoal(newGoal)


    def pickup(self, floor, direction):
        '''
        Decide which elevator will get the task and let him do it.
        It is going to be the closest one not going in the opposite direction.
        If every elevator is going in opposite direction, pick one with shortest goal list.
        '''
        direction = -1 if direction<0 else 1

        bestElev = None
        bestDiff = 9999
        for elevator in self.elevators:
            # find if elevator is suitable
            if (elevator.direction == 0) or \
               (elevator.direction == direction and direction == -1 and elevator.floor > floor) or \
               (elevator.direction == direction and direction == 1 and elevator.floor < floor):
               #if it is best suitable elevator
                if bestDiff > abs(elevator.floor-floor):
                    bestDiff = abs(elevator.floor-floor)
                    bestElev = elevator

        # nothing was found
        if bestElev == None:
            #find the elevator with smallest amount of work
            for elevator in self.elevators:
                if len(elevator.goals) < bestDiff:
                    bestDiff = len(elevator.goals)
                    bestElev = elevator

        # add it to the picked elevator
        bestElev.addGoal(floor)


    def step(self):
        '''
        Perform one step of simulation for each elevator.
        '''
        for elevator in self.elevators:
            elevator.step()



if __name__ == "__main__":
    x = ElevatorControlSystem(3)
    print(x.status())
    x.update(0,0)
    x.update(1,4)
    x.update(2,8)
    print(x.status())
    for i in range(5):
        x.step()
        print(x.status())
    x.pickup(6,1)
    print(x.status())
    x.pickup(6,1)
    print(x.status())
    x.update(0,2,6)
    print(x.status())
    x.pickup(6,1)
    print(x.status())

    for i in range(5):
        x.step()
        print(x.status())
