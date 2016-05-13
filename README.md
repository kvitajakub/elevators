# Elevators

Code is written in Python. Run the script with the example by
```
python elevators.py
```
or open Python command line and play with it.
```
python
```
```
import elevators
x = elevators.ElevatorControlSystem()
x.update(0,0)
x.update(1,4)
print(x.status())
x.pickup(0,1)
x.pickup(3,-1)
```

### Interface

This control system can handle unlimited (reasonable) number of elevators. Specify how many elevators you want in the constructor. Default number is 4 elevators.

`status` method is slightly different from the task given, as it returns the list of goals for each elevator instead of just one.

`update` method has last two parameters optional, so you can decide if you want to teleport the elevator to different location or add a new goal to a specific elevator.

`pickup` and `step`

### Implementation

Each elevator is represented as an object of `Elevator` class, which has necessary data, algorithm sorting goals and simulation code.
`ElevatorControlSystem` serves as controller and handles the input validation.

### Selecting the elevator for pickup.

Method `pickup` chooses the closest elevator, which is free or going in the correct direction as requested. If there is no such elevator, the one with shortest goal list is selected.

### Sorting goals for an elevator.

Goal list of each elevator is sorted to maximize movement in one direction. This means if the elevator is going up, it will go to the highest floor requested, stopping on other floors on the way up, but not going down. Once there are no goals upwards, elevator will go down to the lowest goal.
