"""
IS 597 DS Final Project
Straight or skew
Richie Li
"""

import json
import puzzle
import random
from time import process_time_ns


def solve_puzzle(puz: dict):
    """This function solves the puzzle passed"""
    data = puz["data"]
    print(f'Puzzle with size {data["size"]} is picked, puzzle_id: {puz["id"]}')
    ps = puzzle.Solver(counter={int(k): v for k, v in data['counter'].items()},
                       straight_clues=[data['clue_s'][k] for k in data['clue_s']],
                       oblique_clues=[data['clue_o'][k] for k in data['clue_o']],
                       size=data['size'])
    print(f'Below is the puzzle:\n{ps}\nDo you want to solve it yourself first?(y/n)')
    player_solves: str = input().lower().strip()
    match player_solves:
        case 'y':
            print('Ok, let us see if you can solve it.')
        case 'n':
            print('Ok, I will give you the answer')
        case _:
            print('Umm, I will assume that you want to solve it.')
    if player_solves != 'n':
        while True:
            see_ans = input('Type "ans" to see the answer when you are done.\n')
            if see_ans == 'ans':
                break
            else:
                print('Seems like you do not want the answer:D')
    time_before = process_time_ns()
    ps.find_solutions()
    time_after = process_time_ns()
    print('Total Execution time of the program: {:0.6f} sec.'.format(
        (time_after - time_before) / 1_000_000_000))


if __name__ == '__main__':
    with open('puzzle_data.json', 'r') as file:
        puzzle_data = json.load(file)
    print('Welcome to STRAIGHT OR SKEW')
    while True:
        size_str = input('Please choose the size of puzzle you want to play(3~6), press q to quit:')
        if size_str.lower().strip() == 'q':
            print('See you again!')
            break
        try:
            puzzle_size = int(size_str)
            if puzzle_size < 3 or puzzle_size > 6:
                print('Please enter a number between 3 and 6')
                continue
            puzzle_pick: dict = random.choice(puzzle_data[size_str])
            solve_puzzle(puz=puzzle_pick)
        except ValueError:
            print('Enter a number')
