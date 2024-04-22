"""
To modify
IS 597 DS Final Project
Straight or skew
Richie Li
"""

import puzzle
from time import process_time_ns


if __name__ == '__main__':
    generate = '1'
    solve = '2'
    game_mode = solve
    # sprit_mode = False
    play_with_deterministic = True

    # for spirit_mode in [False, True]:
    for spirit_mode in [False]:
        if game_mode == generate:
            pass
            # while True:
            #     generated = generate_puzzle(height=6, width=6, has_spirit=spirit_mode)
            #     if generated:
            #         break

        elif game_mode == solve:
            puzzles_data = {
                '3x3': {'size': 3,
                        'counter': {puzzle.SQUARE: 3, puzzle.DIAMOND: 3, puzzle.CIRCLE: 3},
                        'clue_s': {
                            puzzle.VERTICAL: [3, 2, 1],
                            puzzle.HORIZONTAL: [3, 1, 2]
                        },
                        'clue_o': {
                            puzzle.N: [3, 3, 1],
                            puzzle.E: [2, 1, 2],
                            puzzle.S: [3, 1, 2],
                            puzzle.W: [2, 2, 1]
                        },
                }
            }

            for name, data in puzzles_data.items():
                time_before = process_time_ns()
                ps = puzzle.Solver(counter=data['counter'],
                                   straight_clues=[data['clue_s'][k] for k in data['clue_s']],
                                   oblique_clues=[data['clue_o'][k] for k in data['clue_o']])

                print('\n\nsolving puzzle "{}"'.format(name))
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
