
''' Slot class: Represents a single slot on the board in any given state. '''

class Slot:

    # Initializes a game board slot with a slot number, dictionary of possible moves, and peg occupancy.
    def __init__(self, num, moves):
        self.num = num
        self.moves = moves
        self.peg = True

    # Determines if a peg currently occupies the slot.
    def has_peg(self):
        return self.peg

    # Vacates a current slot occupancy.
    def remove_peg(self):
        self.peg = False

    # Occupies a vacant slot with a peg.
    def add_peg(self):
        self.peg = True

    # Determines all possible move options for a given slot which is currently occupied with a peg.
    # Returns a dictionary of all possible moves.
    def move_opts(self, jumps):
        move_list = []
        if self.has_peg():
            source = self.num
            poss_jumps = {}
            for jumped in self.moves:
                    destination = self.moves[jumped]
                    if jumps[jumped].has_peg() and not jumps[destination].has_peg():
                        poss_jumps[jumped] = destination
                        move_list.append((source, jumped, destination))
                    
        return move_list