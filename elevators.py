
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

    def update(self, ID, position, newGoal):
        '''
        How can update() change position of the elevator? Physically imposible, but okay.
        Add the new goal to the elevator.
        '''
        if ID < 0 or ID >= len(self.elevators):
            raise Exception('No elevator with ID = ' + str(ID))
        else:
            self.elevators[ID].floor = position
            self.elevators[ID].addGoal(newGoal)


    def pickup(self, floor, direction):
        '''
        Decide which elevator will get the task and let him do it.
        It is going to be the closest one not going in the opposite direction.
        If every elevator is going in opposite direction, pick one with shortest goal list.
        '''
        #TODO DECISION ALGORITHM
        pass


    def step(self):
        '''
        Perform one step of simulation for each elevator.
        '''
        for elevator in self.elevators:
            elevator.step()



if __name__ == "__main__":
    x = ElevatorControlSystem(2)
    print(x.status())
    x.update(1,0,2)
    x.update(1,0,0)
    print(x.status())
    for i in range(4):
        x.step()
        print(x.status())
