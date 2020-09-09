import sys
from enum import Enum
from typing import Optional

WAIT = "WAIT"
BLOCK = "BLOCK"


def err(message, *args, sep=' ', end='\n') -> None:
    print(message, *args, sep=sep, end=end, file=sys.stderr, flush=True)


class Direction(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    NONE = "NONE"


class GridItem:
    def __init__(self, floor: int, position: int) -> None:
        self.floor = floor
        self.position = position

    def __repr__(self):
        return "Floor {} || Position {}".format(self.floor, self.position)


class Elevator(GridItem):
    def __init__(self, floor: int, position: int) -> None:
        super().__init__(floor, position)


class Clone(GridItem):
    def __init__(self, floor: int, position: int, direction: str):
        super().__init__(floor, position)
        self.direction = Direction(direction)

    def __repr__(self):
        return super().__repr__() + " || Direction {}".format(self.direction)

    def is_blocked(self):
        return self.direction == Direction.NONE


class Grid:
    def __init__(self):
        # nb_floors: number of floors
        # width: width of the area
        # nb_rounds: maximum number of rounds
        # exit_floor: floor on which the exit is found
        # exit_pos: position of the exit on its floor
        # nb_total_clones: number of generated clones
        # nb_additional_elevators: ignore (always zero)
        # nb_elevators: number of elevators

        self.nb_floors, self.width, self.nb_rounds, self.exit_floor, self.exit_pos, self.nb_total_clones, self.nb_additional_elevators, self.nb_elevators = [
            int(i) for i in input().split()]

        self.list_elevators = list()
        self.head_clone: Optional[Clone] = None

        for i in range(self.nb_elevators):
            # elevator_floor: floor on which this elevator is found
            # elevator_pos: position of the elevator on its floor
            elevator_floor, elevator_pos = [int(j) for j in input().split()]
            self.list_elevators.append(Elevator(elevator_floor, elevator_pos))

    def __repr__(self):
        return """Nb floors = {}
Width = {}
Nb rounds = {}
Exit floor = {}
Exit position = {}
Nb total clones = {}
Nb elevators = {}""".format(self.nb_floors, self.width, self.nb_rounds, self.exit_floor, self.exit_pos,
                            self.nb_total_clones, self.nb_elevators)

    def update(self) -> None:
        self.head_clone = None
        # clone_floor: floor of the leading clone
        # clone_pos: position of the leading clone on its floor
        # direction: direction of the leading clone: LEFT or RIGHT
        clone_floor, clone_pos, clone_direction = input().split()
        clone_floor = int(clone_floor)
        clone_pos = int(clone_pos)
        self.head_clone = Clone(clone_floor, clone_pos, clone_direction)

    def next_move(self) -> str:
        err(self.head_clone)
        if self.head_clone and not self.head_clone.is_blocked():
            objective_pos = self._get_position_objective()

            suggested_direction = self._get_suggested_direction(objective_pos)

            return self._deduce_next_action(suggested_direction)
        else:
            return WAIT

    def _get_position_objective(self) -> int:
        if self.exit_floor == self.head_clone.floor:
            objective_pos = self.exit_pos
        else:
            elevator_floor = next(elevator
                                  for elevator in self.list_elevators if elevator.floor == self.head_clone.floor)
            objective_pos = elevator_floor.position
        return objective_pos

    def _get_suggested_direction(self, objective_pos: int) -> Direction:
        if objective_pos - self.head_clone.position < 0:
            suggested_direction = Direction.LEFT
        elif objective_pos - self.head_clone.position > 0:
            suggested_direction = Direction.RIGHT
        else:
            suggested_direction = Direction.NONE

        return suggested_direction

    def _deduce_next_action(self, suggested_direction: Direction) -> str:
        if suggested_direction == Direction.NONE:
            return WAIT
        else:
            if suggested_direction == self.head_clone.direction:
                return WAIT
            elif not suggested_direction == self.head_clone.direction:
                return BLOCK
            else:
                return WAIT


grid = Grid()
while True:
    grid.update()
    err(grid)
    action = grid.next_move()
    print(action)
