"""This is a test file to see if the puzzle module (esp. the Solver class) works"""

import puzzle
from time import process_time_ns

puzzles_examples = {
    '0': {
        'size': 3,
        'counter': {puzzle.SQUARE: 3, puzzle.DIAMOND: 3, puzzle.CIRCLE: 3},
        'clue_s': {
            puzzle.VERTICAL: [3, 2, 1],
            puzzle.HORIZONTAL: [3, 1, 2]
        },
        'clue_o': {
            puzzle.N: [3, 3, 1],
            puzzle.E: [2, 1, 3],
            puzzle.S: [3, 1, 2],
            puzzle.W: [2, 2, 1]
        },
    },
    '1': {
        'size': 4,
        'counter': {puzzle.SQUARE: 6, puzzle.DIAMOND: 6, puzzle.CIRCLE: 4},
        'clue_s': {
            puzzle.VERTICAL: [2, 3, 2, 3],
            puzzle.HORIZONTAL: [2, 3, 2, 3]
        },
        'clue_o': {
            puzzle.N: [2, 3, 4, 1],
            puzzle.E: [3, 2, 3, 2],
            puzzle.S: [2, 3, 1, 3],
            puzzle.W: [3, 2, 2, 4]
        },
    },
    '2': {
        'size': 5,
        'counter': {puzzle.SQUARE: 9, puzzle.DIAMOND: 7, puzzle.CIRCLE: 9},
        'clue_s': {
            puzzle.VERTICAL: [4, 3, 2, 4, 5],
            puzzle.HORIZONTAL: [3, 5, 5, 4, 1]
        },
        'clue_o': {
            puzzle.N: [4, 3, 2, 4, 3],
            puzzle.E: [3, 4, 4, 3, 4],
            puzzle.S: [4, 3, 3, 3, 4],
            puzzle.W: [3, 3, 3, 2, 2]
        },
    },
}

if __name__ == '__main__':

    for name, data in puzzles_examples.items():
        time_before = process_time_ns()
        ps = puzzle.Solver(counter=data['counter'],
                           straight_clues=[data['clue_s'][k] for k in data['clue_s']],
                           oblique_clues=[data['clue_o'][k] for k in data['clue_o']],
                           size=data['size'])

        print(f'\n\nsolving size {data["size"]} puzzle id "{name}"')
        # print(ps)

        puzzle_solutions = ps.find_solutions()

        if puzzle_solutions == 1:
            print('Puzzle is VALID.')
        else:
            print('Puzzle is NOT VALID.')

        time_after = process_time_ns()
        print('Total Execution time: {:0.6f} sec.'.format(
            (time_after - time_before) / 1_000_000_000))
