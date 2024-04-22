"""
This is the module that contains objects for the puzzle
"""

# from collections import Counter
from typing import Union, List, Tuple


Shape = int
SHAPES = [EMPTY, SQUARE, DIAMOND, CIRCLE] = range(4)
SHAPE_SYMBOL = ['_', '◼', '◆', '⬤']  # https://www.alt-codes.net/
STRAIGHTS = [VERTICAL, HORIZONTAL] = range(2)
DIRECTIONS = [N, E, S, W] = range(4)  # Used in determine oblique clue directions
# OBLIQUES = [NW, NE, SE, SW] = range(4, 8)  # heading direction (from cell)


def get_shape_str(shape: Shape) -> str:
    return SHAPE_SYMBOL[shape]


class Cell:
    """Cell
    >>> c = Cell(shape=SQUARE)
    >>> print(f'{c}')
    ◼
    """
    def __init__(self, row=None, col=None, shape=EMPTY):
        self.row = row
        self.col = col
        self.shape = shape

    def __str__(self):
        return get_shape_str(self.shape)


class Board:
    """This is a board class
    >>> b = Board(counter={SQUARE: 5, DIAMOND: 3, CIRCLE: 1})
    >>> print(b)
    This is a size 3 board:
    COUNTER: Square: 5, Diamond: 3, Circle: 1
    0000000
    0_ _ _0
    0     0
    0_ _ _0
    0     0
    0_ _ _0
    0000000
    <BLANKLINE>
    """
    def __init__(self, counter: dict, straight_clues, oblique_clues, size=3):
        self.size = size
        self.grid = [[Cell(row=row, col=col, shape=EMPTY) for col in range(size)] for row in range(size)]
        self.counter = counter
        self.straight = [[0 for _ in range(size)] for _ in range(2)]  # [VERTICAL, HORIZONTAL]
        self.oblique = [[0 for _ in range(size)] for _ in range(4)]
        self.straight_clues = straight_clues
        self.oblique_clues = oblique_clues
        if self.straight_clues is None or self.oblique_clues is None:
            raise ValueError('No clues given')
        """
        oblique is the diagonals which separated into 4 sides
        xxxo
        a  o
        a  o
        abbb
        """

    def __str__(self):
        header = f'This is a size {self.size} board:\n'
        shape_counts = (f'COUNTER: Square: {self.counter[SQUARE]}, '
                        f'Diamond: {self.counter[DIAMOND]}, '
                        f'Circle: {self.counter[CIRCLE]}\n')
        grid_str = ''
        for i in range(self.size):
            grid_str += f'{self.oblique_clues[N][i]}{self.straight_clues[VERTICAL][i]}'
        grid_str += f'{self.oblique_clues[E][0]}\n'
        for i in range(self.size):
            grid_str += f'{self.straight_clues[HORIZONTAL][i]}'
            for j in range(self.size):
                if j < self.size-1:
                    grid_str += f'{self.grid[i][j]} '
                else:
                    grid_str += f'{self.grid[i][j]}'
            grid_str += f'{self.straight_clues[HORIZONTAL][i]}\n'
            if i < self.size-1:
                grid_str += (f'{self.oblique_clues[W][(self.size-1)-i]}'
                             f'{" "*(self.size*2-1)}{self.oblique_clues[E][i+1]}\n')
        grid_str += f'{self.oblique_clues[W][0]}'
        for i in range(self.size):
            grid_str += f'{self.straight_clues[VERTICAL][i]}{self.oblique_clues[S][(self.size-1)-i]}'
        board_str = header + shape_counts + grid_str + '\n'
        return board_str

    def is_full(self) -> bool:
        for ci in self.grid:
            for cj in ci:
                if cj.shape == EMPTY:
                    return False
        return True

    def get_next_empty_cell(self) -> Union[Cell, None]:
        for ci in self.grid:
            for cj in ci:
                if cj.shape == EMPTY:
                    return cj
        return None

    def modify_oblique_clue(self, di_list: List[Tuple], mode: str) -> None:
        """
        As title
        :param di_list: A list of direction and index of oblique clues, e.g., [(N, 0), (E, 0), (S, 0), (W, 0)]
        :param mode: to add (fill puzzle) or subtract (backtrack)
        """
        for d, i in di_list:
            match mode:
                case '+':  # todo: if other false but this true must cancel addition
                    self.oblique[d][i] += 1
                case '-':
                    self.oblique[d][i] -= 1

    def find_cell_obliques(self, cell: Cell) -> List[Tuple]:
        """As title"""
        rc_diff = cell.row - cell.col
        rc_sum = cell.row + cell.col
        c1 = abs(rc_diff)
        c2 = self.size - c1
        c3 = abs(rc_sum - (self.size-1))
        c4 = self.size - c3
        obliques = None
        # Antidiag is adding, Diagonal is subtracting
        if rc_diff > 0:
            # In SW corner
            if rc_sum < self.size - 1:
                # W
                obliques = [(N, c4), (S, c1), (W, c3), (W, c2)]
            elif rc_sum > self.size - 1:
                # S
                obliques = [(E, c3), (S, c1), (S, c4), (W, c2)]
            elif rc_sum == self.size - 1:
                # On antidiag line
                obliques = [(E, 0), (S, c1), (W, 0), (W, c2)]
        elif rc_diff < 0:
            # In NE corner
            if rc_sum < self.size - 1:
                # N
                obliques = [(N, c1), (N, c4), (E, c2), (W, c3)]
            elif rc_sum > self.size - 1:
                # E
                obliques = [(N, c1), (E, c3), (E, c2), (S, c4)]
            elif rc_sum == self.size - 1:
                # On antidiag line
                obliques = [(N, c1), (E, 0), (E, c2), (W, 0)]
        elif rc_diff == 0:
            # On Diagonal Line
            if rc_sum < self.size - 1:
                # NW
                obliques = [(N, 0), (N, c4), (S, 0), (W, c3)]
            elif rc_sum > self.size - 1:
                # SE
                obliques = [(N, 0), (E, c3), (S, 0), (S, c4)]
            elif rc_sum == self.size - 1:
                # Mid
                obliques = [(N, 0), (E, 0), (S, 0), (W, 0)]
        return obliques

    def is_valid_puzzle(self, cell: Cell) -> bool:
        """DONE
        Let shape radiate to the edge to add, if invalid, subtract and return False
        :param cell:
        :return:
        """
        if cell.shape == SQUARE or cell.shape == CIRCLE:
            if self.straight[VERTICAL][cell.col] + 1 > self.straight_clues[VERTICAL][cell.col]:
                return False
            self.straight[VERTICAL][cell.col] += 1
            if self.straight[HORIZONTAL][cell.row] + 1 > self.straight_clues[HORIZONTAL][cell.row]:
                return False
            self.straight[HORIZONTAL][cell.row] += 1

        if cell.shape == DIAMOND or cell.shape == CIRCLE:
            result_oblique = True
            obliques_list: List[Tuple] = self.find_cell_obliques(cell=cell)  # e.g., [(N, 0), (E, 0), (S, 0), (W, 0)]
            if obliques_list is None:
                raise ValueError('obliques_list is None')
            for d, i in obliques_list:
                result_oblique &= (self.oblique[d][i] + 1 <= self.oblique_clues[d][i])
                if not result_oblique:
                    return False
            self.modify_oblique_clue(di_list=obliques_list, mode='+')

        return True

    def place_shape(self, cell: Cell):
        self.grid[cell.row][cell.col] = cell

        if not self.is_valid_puzzle(cell=cell):
            self.grid[cell.row][cell.col].shape = EMPTY
            return False

        self.counter[cell.shape] -= 1
        return True


class Solver(Board):
    """Solver"""

    def __init__(self, counter: dict, straight_clues, oblique_clues):
        super().__init__(counter, straight_clues, oblique_clues)
        self.solutions: List = []
        self.moves: List[Cell] = []

    def __str__(self):
        return super().__str__()

    def backtrack(self) -> None:  # todo: smth wrong here
        """backtrack"""
        last_cell = self.moves.pop() if len(self.moves) else None
        if last_cell is None:
            raise ValueError('Backtracked all the way to beginning. No more solutions.')
        self.counter[last_cell.shape] += 1

        # Subtract edge numbers
        self.straight[VERTICAL][last_cell.col] -= 1
        self.straight[HORIZONTAL][last_cell.row] -= 1
        obliques_list: List[Tuple] = self.find_cell_obliques(cell=last_cell)
        self.modify_oblique_clue(di_list=obliques_list, mode='-')

        # Try placing a shape
        # placed = False
        while True:
            if last_cell.shape in SHAPES[1:-1] and self.counter[last_cell.shape+1]:
                last_cell.shape += 1
                placed = self.place_shape(cell=last_cell)
                if placed:
                    break
                else:
                    continue
            elif last_cell.shape in SHAPES[1:-2] and self.counter[last_cell.shape+2]:  # Square to Circle
                last_cell.shape += 2
                placed = self.place_shape(cell=last_cell)
                if placed:
                    break
                else:
                    continue
            # elif last_cell.shape == SHAPES[-1]:
            #     self.backtrack()
            #     break
            else:
                self.backtrack()
                break
                # print(f'cell shape is {last_cell.shape}')
                # raise ValueError('Last cell shape???')  #  error has led to here once
        return

    def find_solutions(self) -> int:
        """
        The method to solve the puzzle
        :return: The number of solutions
        """
        while not self.is_full():
            try:
                cell = self.get_next_empty_cell()
                if cell is None:
                    print("Didn't get the next cell")
                    break

                placed = False
                for s in SHAPES[1:]:
                    if self.counter[s]:
                        cell.shape = s
                        placed = self.place_shape(cell=cell)
                        if placed:
                            print(f'Placed move {len(self.moves)}:\n{self}\n')
                            self.moves.append(cell)
                            break
                if not placed:
                    self.backtrack()

                if self.is_full():
                    # Solved
                    solution = str(self)
                    self.solutions.append(solution)
                    print(f'\nGOT SOLUTION #{len(self.solutions)}:\n {solution}')
                    if len(self.solutions) > 1:
                        # Multiple Solutions
                        break
                    # Backtrack to see if there are multiple answers
                    self.backtrack()
            except ValueError as ex:
                if ex.args[0] == 'Backtracked all the way to beginning. No more solutions.':
                    break
                else:
                    raise ex  # something unexpected happened.
        return len(self.solutions)


class Generator(Board):
    """Generator"""
