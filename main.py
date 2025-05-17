from cubes import *
from random import shuffle
from random import randint



def run_round(race_track, cubes, debug=False, round_counter=0, round=1):
    if round_counter != 0 or round ==2:
        # Shuffle cubes at the start of each round, except the first round (first round is already shuffled) and starting stack is inverse order of roll order
        shuffle(cubes)
    #Find any forced last mover for this round and moved them to the end of the list
    cubes = [cube for cube in cubes if not cube.move_last_next_round] + [cube for cube in cubes if cube.move_last_next_round]

    for i, cube in enumerate(cubes):
        #Move all cubes forward by their dice rolls, if they have other cubes on top of them the will move with them
        if debug:
            print(f"{cube.name} is moving")
        if i==0:
            cube.first_mover = True  # Mark the first mover
        if i == len(cubes) - 1:
            cube.last_moved = True  # Mark the last moved cube
        cube.execute_move(race_track)
        for j, otherCube in enumerate(cubes):
            if j != i:
                otherCube.after_opponent_move(race_track, cube)
        
    for cube in cubes:
        cube.end_round(race_track)
        cube.last_moved = False  # Reset last moved status for all cubes
        cube.first_mover = False  # Reset first mover status for all cubes


def main(cubes, race_track, debug=False,round=1):
    if debug:
        print(f"Initial race track:")
        print_race_track(race_track)
    round_count = 0
    while race_track[-1] == []:
        if debug:
            print(f"\n--- Round {round_count + 1} ---")
        run_round(race_track, cubes, debug=debug, round_counter=round_count, round=round)
        round_count += 1
    return race_track[-1][-1] # It looks like to last in the stack is the winner


if __name__ == "__main__":
    repetitions = 10000
    debug = False
    track_length = 24
    round = 2  # Set to 1 for the first round, 2 for the second round

    cubes = [
            # ShorekeeperCube(debug=debug),
            # CarlottaCube(debug=debug),
            # CalcharoCube(debug=debug),
            # ChangliCube(debug=debug),
            # CamellyaCube(debug=debug),
            # JinhsiCube(debug=debug),
            RocciaCube(debug=debug),
            BrantCube(debug=debug),
            CantarellaCube(debug=debug),
            ZaniCube(debug=debug),
            CartethyaCube(debug=debug),
            PhoebeCube(debug=debug),

    ]
    # Define starting positions for each cube in round 2
    starting_positions = {
        "RocciaCube": (3, 0),
        "BrantCube": (2, 0),
        "CantarellaCube": (2, 1),
        "ZaniCube": (1, 0),
        "CartethyaCube": (0, 0),
        "PhoebeCube": (1, 1),
    }


    payout ={
        # "CarlottaCube": 1.15,
        # "CalcharoCube": 1.7,
        # "ShorekeeperCube": 1.44,
        # "ChangliCube": 1.84,
        # "JinhsiCube": 1.58,
        # "CamellyaCube": 1.97,
        "RocciaCube": 1.34,
        "BrantCube": 1.6,
        "CantarellaCube": 1.78,
        "ZaniCube": 1.61,
        "CartethyaCube": 1.88,
        "PhoebeCube": 1.79,
        
    }


    results = {cube.name: 0 for cube in cubes}
    for i in range(repetitions):
        cubes = [
            # ShorekeeperCube(debug=debug),
            # CarlottaCube(debug=debug),
            # CalcharoCube(debug=debug),
            # ChangliCube(debug=debug),
            # CamellyaCube(debug=debug),
            # JinhsiCube(debug=debug),
            RocciaCube(debug=debug),
            BrantCube(debug=debug),
            CantarellaCube(debug=debug),
            ZaniCube(debug=debug),
            CartethyaCube(debug=debug),
            PhoebeCube(debug=debug),
        ]

        
        print(f"Running simulation {i+1}")
        
        #Round 1
        if round == 1:
            shuffle(cubes)
            race_track = [[] for _ in range(track_length)]
            race_track[0] = cubes.copy()  # Place all cubes at the start
            race_track[0].reverse()  # Reverse the order to match the stack positions
            for i, cube in enumerate(cubes):
                cube.position = 0
                cube.stack_position = len(cubes)-i-1  # Stack position is the reverse of the index in the initial list
        #Round 2
        elif round == 2:
            race_track = [[] for _ in range(track_length+4)]
            for cube in cubes:
                cube.position = starting_positions[cube.name][0]
                cube.stack_position = starting_positions[cube.name][1]
                race_track[cube.position].append(cube)  # Place each cube at its starting position
            race_track = [sorted(pad, key=lambda x: x.stack_position, reverse=False) for pad in race_track]


        winner = main(cubes=cubes, race_track=race_track, debug=debug, round=round)
        results[winner.name] += 1
        print(f"Winner of simulation {i+1}: {winner.name}")
    print(f"Results after {repetitions} simulations: {results}")
    #Expected payout
    win_rates = {cube.name: results[cube.name] / repetitions for cube in cubes}
    print(f"Win rates after {repetitions} simulations: {win_rates}")
    expected_payout = {cube.name: win_rates[cube.name] * payout[cube.name] + 0.8*(1-win_rates[cube.name]) for cube in cubes} #80% refund for not winning
    print(f"Expected payout after {repetitions} simulations: {expected_payout}")

    


