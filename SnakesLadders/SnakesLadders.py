"""
Finite State Machine for Snakes and Ladders game
Kind character codes:
    S = Snake, L = Ladder (aka Chute), B = Blank
"""
# coding: utf-8

import random
import pprint

class State(object):
    def __init__(self, ix):
        self.index = ix
        self.link = None  # placeholder, not None if Snake or Ladder
        self.kind = None

    def process(self):
        """Action when landed upon"""
        if self.link:
            if self.link > self.index:
                # ! this is inefficient because it gets re-updated every time
                # this method is called!
                self.kind = 'L'
                print("Ladder from {0} -> {1}".format(self.index, self.link))
                return self.link
            else:
                self.kind = 'S'
                print("Snake from {0} -> {1}".format(self.index, self.link))
                return self.link
        else:
            # link is None: "Blank" = not a snake or ladder
            self.kind = 'B'
            return self.index


class GameFSM(object):
    def __init__(self, n):
        # list of State objects for each position on the board
        self.all_states = []
        # current position of player on board
        self.position = 0
        # size of board
        self.n = n
        # make empty board states for each position
        # (snake and ladder positions must be added later)
        for ix in range(n+1):
            blank_state = State(ix)
            self.all_states.append(blank_state)
        # record of moves, die rolls, and snake/ladder use
        self.records = []

    def move_and_record(self, die):
        """die is an integer
        """
        start_pos = self.position
        inter_pos = self.position + die
        try:
            state_obj = self.all_states[inter_pos]
        except IndexError:
            # moved off the end of the board
            kind = 'B'
            final_pos = self.n
        else:
            final_pos = state_obj.process()
            kind = state_obj.kind
        self.position = final_pos
        # all this could be written more consisely as
        #self.position = self.all_states[self.position+die].process()
        record = {'start': start_pos,
                  'die': die,
                  'kind': kind,
                  'end': self.position}
        self.records.append(record)

    def run(self):
        """
        Run one whole game
        """
        print("Starting game!")
        while self.position < self.n:
            # roll die
            die = rollDie()
            print("Die={}".format(die))
            # move based on die roll and record results
            self.move_and_record(die)
            print("New position is {}".format(self.position))
        print("Game over!")


def rollDie():
    return random.randint(1, DIE_SIDES)

# Global constant in caps
DIE_SIDES = 4

game = GameFSM(16)


# Make ladders
game.all_states[2].link = 10
game.all_states[8].link = 14

# Make snakes
game.all_states[11].link = 4
game.all_states[15].links = 6

#print(game.all_states)

game.run()

pprint.pprint(game.records)

# Find total number of moves from records

def count_moves(records):
    return len(records)

# Find number of snakes or ladders used in game

def count_snakes_and_ladders(records):
    s = 0
    l = 0
    for i in records:
        if (i["kind"] == 'L'):
            l += 1
        elif (i["kind"] == 'S'):
            s += 1
    return (s, l)

print ("The number of snakes is %i. The number of ladders is %i" % (count_snakes_and_ladders(game.records) ))
print ("The total number of moves is %i" % (count_moves(game.records)))
