from random import randint,random

def print_race_track(race_track):
    for i, pad in enumerate(race_track):
        print(f"pad {i}: {pad}")

class BaseCube:
    def __init__(self,name="BaseCube",debug=False):
        self.debug = debug
        self.position = 0
        self.stack_position = 0
        self.name = name
        self.last_moved = False  # Track if this cube was the last to move
        self.move_last_next_round = False  # Track if this cube should move last next round
        self.first_mover = False
    def roll_dice(self):
        return randint(1, 3)
    def __repr__(self):
        return f"({self.name}, {self.position}, {self.stack_position})"
    def __str__(self):
        return f"{self.name} at position {self.position} with stack position {self.stack_position}"
    def execute_move(self, race_track, dice_roll=None):
        if dice_roll is None:
            dice_roll = self.roll_dice()
        stacked_participants = race_track[self.position][self.stack_position:]
        race_track[self.position] = race_track[self.position][:self.stack_position]
        for stacked_participant in stacked_participants:
            stacked_participant.position += dice_roll
            if stacked_participant.position >= len(race_track):
                stacked_participant.position = len(race_track) - 1
                stacked_participant.stack_position = len(race_track[-1])
                race_track[-1].append(stacked_participant)
                
            else:
                stacked_participant.stack_position = len(race_track[stacked_participant.position]) 
                race_track[stacked_participant.position].append(stacked_participant)
        if self.debug:
            print(f"{self.name} moved {dice_roll} spaces to position {self.position + dice_roll}")
            print_race_track(race_track)

    def end_round(self, race_track):
        pass
    def after_opponent_move(self, race_track, opponent_cube):
        pass

class ShorekeeperCube(BaseCube):
    def __init__(self, name="ShorekeeperCube", debug=False):
        super().__init__(name, debug=debug)

    def roll_dice(self):
        return randint(2, 3)
    
class CarlottaCube(BaseCube):
    def __init__(self, name="CarlottaCube", debug=False):
        super().__init__(name, debug=debug)

    def execute_move(self, race_track, dice_roll=None):
        #28% chance to move twice
        if dice_roll is None:
            dice_roll = self.roll_dice()
        if random() < 0.28:
            if self.debug:
                print(f"{self.name} activated skill and will move twice")
            super().execute_move(race_track, dice_roll)
        super().execute_move(race_track, dice_roll)
    
class CalcharoCube(BaseCube):
    def __init__(self, name="CalcharoCube", debug=False):
        super().__init__(name, debug=debug)

    #If ranked last at the start of turn move 3 more spaces 
    def execute_move(self, race_track, dice_roll=None):
        if dice_roll is None:
            dice_roll = self.roll_dice()
        for pad in race_track:
            if pad == []:
                continue
            if len(pad) > 0:
                if pad[0] == self:
                    if self.debug:
                        print(f"{self.name} activated skill and will move 3 additional spaces")
                    dice_roll += 3
                break
        super().execute_move(race_track, dice_roll=dice_roll)

class ChangliCube(BaseCube):
    def __init__(self, name="ChangliCube", debug=False):
        super().__init__(name, debug=debug)

    def end_round(self, race_track):
        #65% chance to move last next round if there are other cubes below her, assuming it only applies at the end of the round
        if self.stack_position > 0 and random() < 0.65:
            if self.debug:
                print(f"{self.name} activated skill and will move last next round")
            self.move_last_next_round = True
        else:
            self.move_last_next_round = False

class CamellyaCube(BaseCube):
    def __init__(self, name="CamellyaCube", debug=False):
        super().__init__(name, debug=debug)

    def execute_move(self, race_track, dice_roll=None):
        # There is a 50% chance to move as many positions as cubes are in her stack wihtout moving others in the stack
        if random() < 0.5:

            if dice_roll is None:
                dice_roll = self.roll_dice()
            dice_roll += len(race_track[self.position])-1 #Not counting herself
            original_position = self.position
            # Remove herself from the current position
            race_track[original_position].pop(self.stack_position)
            # Resync the stack position for other cubes in the stack
            for i, cube in enumerate(race_track[original_position]):
                cube.stack_position = i
            self.position += dice_roll
            if self.position >= len(race_track): 
                self.position = len(race_track) - 1
                self.stack_position = len(race_track[-1])
                race_track[-1].append(self)
                
            else:
                self.stack_position = len(race_track[self.position])
                race_track[self.position].append(self)
            if self.debug:
                print(f"{self.name} activated skill and will move {self.stack_position + 1} positions forward in addition to the dice roll {dice_roll}, without moving others in the stack")
                print_race_track(race_track) 
        else:
            super().execute_move(race_track, dice_roll)

class JinhsiCube(BaseCube):
    def __init__(self, name="JinhsiCube", debug=False):
        super().__init__(name, debug=debug)

    # Jinhsi moves to the top of the stack if an opponent is moved on top of her stack position with 40% chance
    #I don't know when does her skill get checked but I am assuming after every move ending at her stack position, same wording as changli but changli makes sense to apply only at the end of round while Jinhsi does activate mid round)
    #There's just too many posibilities (after one cube ends up directly on top of her, after a cube ends up anywhere on top of her, after all cubes have moved (discarded because in round one it happens mid round)
    def after_opponent_move(self, race_track, opponent_cube):
        if random() < 0.4 and opponent_cube.position == self.position and opponent_cube.stack_position > self.stack_position:
            if self.debug:
                print(f"{self.name} activated skill and moved to the top of the stack at position {self.position}")
            race_track[self.position].remove(self)
            self.stack_position = len(race_track[self.position])
            race_track[self.position].append(self)
            # Resync stack positions for all cubes in the pad

            for i, cube in enumerate(race_track[self.position]):
                cube.stack_position = i

class RocciaCube(BaseCube):
    def __init__(self, name="RocciaCube", debug=False):
        super().__init__(name, debug=debug)


    def execute_move(self, race_track, dice_roll=None):
        # Roccia moves two extra spaces if she is the last to move
        if self.last_moved:
            if self.debug:
                print(f"{self.name} activated skill and will move 2 spaces forward")
            super().execute_move(race_track, dice_roll=self.roll_dice() + 2)
        else:
            super().execute_move(race_track)

class BrantCube(BaseCube):
    def __init__(self, name="BrantCube", debug=False):
        super().__init__(name, debug=debug)

    #Brant moves 2 spaces forward if he is the first to move
    def execute_move(self, race_track, dice_roll=None):
        if self.first_mover:
            if self.debug:
                print(f"{self.name} activated skill and will move 2 spaces forward")
            super().execute_move(race_track, dice_roll=self.roll_dice() + 2)
        else:
            super().execute_move(race_track)

class CantarellaCube(BaseCube):
    def __init__(self, name="CantarellaCube", debug=False):
        super().__init__(name, debug=debug)
        self.activated_skill = False


    #The first time she passes by other cubes she stacks with them and carries them with her. Once per race
    def execute_move(self, race_track, dice_roll=None):
        if dice_roll is None:
            dice_roll = self.roll_dice()
        if self.activated_skill == False:
            stacked_participants = race_track[self.position][self.stack_position:]
            for j in range(dice_roll):
                if len(race_track[self.position+j]) > 0:
                    if self.activated_skill == False:
                        if self.debug:
                            print(f"{self.name} activated skill and will stack with {len(race_track[self.position+j])} cubes") 
                        stacked_participants = race_track[self.position+j]+stacked_participants
                        race_track[self.position+j] = []
                    self.activated_skill = True
        else:
            stacked_participants = race_track[self.position][self.stack_position:]
        race_track[self.position] = race_track[self.position][:self.stack_position]
        for stacked_participant in stacked_participants:
            stacked_participant.position = self.position + dice_roll
            if stacked_participant.position >= len(race_track):
                stacked_participant.position = len(race_track) - 1
                stacked_participant.stack_position = len(race_track[-1])
                race_track[-1].append(stacked_participant)
            else:
                stacked_participant.stack_position = len(race_track[stacked_participant.position]) 
                race_track[stacked_participant.position].append(stacked_participant)
        if self.debug:
            print(f"{self.name} moved {dice_roll} spaces to position {self.position + dice_roll}")
            print_race_track(race_track)

class ZaniCube(BaseCube):
    def __init__(self, name="ZaniCube", debug=False):
        super().__init__(name, debug=debug)
        self.activated_skill = False


    #Zani can only roll 1 or 3, when moving with a stacked opponent she moves two extra spaces next round with 40% chance
    def roll_dice(self):
        if random() < 0.5:
            return 1
        else:
            return 3

    def execute_move(self, race_track, dice_roll=None):
        if dice_roll is None:
            dice_roll = self.roll_dice()
        if self.activated_skill == True:
            dice_roll += 2
            self.activated_skill == False

        stacked_participants = race_track[self.position][self.stack_position:]
        if len(stacked_participants) > 1 and random() < 0.4:
            if self.debug:
                print(f"{self.name} activated skill and will move 2 spaces forward next round")
            self.activated_skill = True
        race_track[self.position] = race_track[self.position][:self.stack_position]
        for stacked_participant in stacked_participants:
            stacked_participant.position += dice_roll
            if stacked_participant.position >= len(race_track):
                stacked_participant.position = len(race_track) - 1
                stacked_participant.stack_position = len(race_track[-1])
                race_track[-1].append(stacked_participant)
                
            else:
                stacked_participant.stack_position = len(race_track[stacked_participant.position]) 
                race_track[stacked_participant.position].append(stacked_participant)
        if self.debug:
            print(f"{self.name} moved {dice_roll} spaces to position {self.position + dice_roll}")
            print_race_track(race_track)

class CartethyaCube(BaseCube):
    def __init__(self, name="CartethyaCube", debug=False):
        super().__init__(name, debug=debug)
        self.activated_skill = False


    #If ranked last after own turn, 60% chance to advance 2 extra pads in all remaining rounds
    def execute_move(self, race_track, dice_roll=None):
        if self.activated_skill == True:
            dice_roll = self.roll_dice()+2
            super().execute_move(race_track, dice_roll=dice_roll)
        else:
            super().execute_move(race_track)
            for pad in race_track:
                if pad == []:
                    continue
                if len(pad) > 0:
                    if pad[0] == self:
                        if random() < 0.6:
                            if self.debug:
                                print(f"{self.name} activated skill and will move 2 spaces forward for the remaining rounds")
                            self.activated_skill = True
                    break

class PhoebeCube(BaseCube):
    def __init__(self, name="PhoebeCube", debug=False):
        super().__init__(name, debug=debug)


    #%50 chance to move an extra space
    def execute_move(self, race_track, dice_roll=None):
        if dice_roll is None:
            dice_roll = self.roll_dice()
        if random() < 0.5:
            dice_roll += 1
            if self.debug:
                print(f"{self.name} activated skill and will move 1 extra space")
        super().execute_move(race_track, dice_roll=dice_roll)
