"""
To modify
IS 597 DS Final Project
Straight or skew
Richie Li
"""

import puzzle
from time import process_time_ns

def solve_puzzle():
    # todo: Input board and solve
    pass


if __name__ == '__main__':
    generate = '1'
    solve = '2'
    game_mode = solve

    if game_mode == generate:
        pass
        # while True:
        #     generated = generate_puzzle(height=6, width=6, has_spirit=spirit_mode)
        #     if generated:
        #         break

    elif game_mode == solve:
        puzzles_data = {
            '0': {'size': 3,
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
            '1': {'size': 3,
                  'counter': {puzzle.SQUARE: 5, puzzle.DIAMOND: 2, puzzle.CIRCLE: 2},
                  'clue_s': {
                      puzzle.VERTICAL: [3, 2, 2],
                      puzzle.HORIZONTAL: [2, 2, 3]
                  },
                  'clue_o': {
                      puzzle.N: [2, 1, 1],
                      puzzle.E: [2, 2, 0],
                      puzzle.S: [3, 1, 1],
                      puzzle.W: [2, 0, 2]
                  },
                  },
            '2': {'size': 4,
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
                  }
        }

        for name, data in puzzles_data.items():
            time_before = process_time_ns()
            ps = puzzle.Solver(counter=data['counter'],
                               straight_clues=[data['clue_s'][k] for k in data['clue_s']],
                               oblique_clues=[data['clue_o'][k] for k in data['clue_o']],
                               size=data['size'])

            print('\n\nsolving puzzle id "{}"'.format(name))
            print(ps)

            puzzle_solutions = ps.find_solutions()
            time_after = process_time_ns()
            print('Total Execution time: {:0.6f} sec.'.format(
                (time_after - time_before) / 1_000_000_000))

            if puzzle_solutions == 1:
                print('Puzzle "{}" is VALID.'.format(name))
            else:
                print('Puzzle "{}" is NOT VALID.'.format(name))
    else:
        print('??? What game mode do you want???')
