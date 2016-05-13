
class Elevator:

    def __init__(self):
        self.floor = 0
        self.goals = [ None ]
        self.direction = 0

    def status(self):
        # return [self.floor, self.goals[0]]
        return [self.floor] + [self.goals]

    def addGoal(self, goal):
        #skip the None, keep it at the end
        self.goals.insert(-1,goal)
        self.sortGoals()

    def sortGoals(self):
        '''
        Some sort of scheduling system for one elevator, probably trying to maximize movement in one direction.
        Remove redundancies, each floor only once.
        '''
        # SORTING ALGORITHM
        lowerGoals = []
        higherGoals = []
        #remove none and duplicates
        self.goals.remove(None)
        self.goals = list(set(self.goals))

        #split into two lists
        for goal in self.goals:
            if goal > self.floor:
                higherGoals.append(goal)
            elif goal < self.floor:
                lowerGoals.append(goal)

        #sort lists properly
        higherGoals.sort()
        lowerGoals.sort()
        lowerGoals.reverse()

        #decide how to add them back
        if self.direction == 1:
            self.goals = higherGoals + lowerGoals
        else:
            self.goals = lowerGoals + higherGoals

        #return None back
        self.goals.append(None)

        #set the direction based of the first goal
        if self.goals[0] != None:
            self.direction = -1 if self.floor > self.goals[0] else 1
        else:
            self.direction = 0


    def step(self):
        '''
        Perform one step of simulation.
        '''
        # if elevator have task, move
        if self.goals[0] != None:
            self.floor += self.direction
            if self.floor == self.goals[0]:
                #remove task if elevator reached the destination
                self.goals.pop(0)
                if self.goals[0] != None:
                    #change direction if next task is in opposite direction
                    self.direction = -1 if self.floor > self.goals[0] else 1
                else:
                    #or stop if there are no tasks
                    self.direction = 0



class ElevatorControlSystem:
    def __init__(self, elevators=4):
        '''
        Elevator Control system need to know how many elevators have to be created. Specify as parameter.
        '''
        self.elevators = []
        for i in range(elevators):
            self.elevators.append(Elevator())


    def status(self):
        '''
        Return the status of the elevators  as list of lists
        [
            [ID, CurrentFloor, goalList],
            [ID, CurrentFloor, goalList],
            [ID, CurrentFloor, goalList],
            ...
        ]
        '''
        data = []
        for i in range(len(self.elevators)):
            data.append([i] + self.elevators[i].status())
        return data


    def update(self, ID, floor=None, newGoal=None):
        '''
        Update the elevator with ID. Put it on floor speficied and add a new goal to the list.
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
        #change the input range
        direction = -1 if direction<0 else 1

        bestElev = None
        bestDiff = 9999
        for elevator in self.elevators:
            # find if elevator is suitable
            if (elevator.direction == 0) or \
               (elevator.direction == direction and direction == -1 and elevator.floor > floor) or \
               (elevator.direction == direction and direction == 1 and elevator.floor < floor):
               #pick it if it is the best suitable elevator
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

        # add the job to the picked elevator
        bestElev.addGoal(floor)


    def step(self):
        '''
        Perform one step of simulation for each elevator.
        '''
        for elevator in self.elevators:
            elevator.step()


if __name__ == "__main__":
    x = ElevatorControlSystem(3)
    x.update(0,0)
    x.update(1,4)
    x.update(2,8)
    print(x.status())

    x.pickup(0,1)
    x.pickup(3,-1)
    x.pickup(6,1)
    x.pickup(5,-1)
    x.pickup(1,1)

    print(x.status())

    for i in range(3):
        x.step()
        print(x.status())

    x.update(0,newGoal=5)
    x.update(1,newGoal=0)
    x.update(2,newGoal=7)

    print(x.status())

    for i in range(3):
        x.step()
        print(x.status())

    x.pickup(0,1)
    x.pickup(3,-1)
    x.pickup(6,1)
    x.pickup(6,-1)
    x.pickup(5,-1)
    x.pickup(1,1)

    print(x.status())

    for i in range(3):
        x.step()
        print(x.status())
