
import random
import slot

''' Board class: Represents a game board in any given state. '''

class Board:

    # Initializes a game board with a defeat, an array of board states (nodes),
    # an array of discovered nodes, an array of processed nodes, an array of all slot numbers,
    # an array to store previous moves, and a dictionary of all possible moves for every slot.
    def __init__(self):
        self.victory = False
        self.open = []
        self.closed = []
        self.i_states = []
        self.pegs = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        self.history = []
        self.jumps = [slot.Slot(0, {1 : 3, 2 : 5}),
                      slot.Slot(1, {3 : 6, 4 : 8}),
                      slot.Slot(2, {4 : 7, 5 : 9}),
                      slot.Slot(3, {4 : 5, 1 : 0, 6 : 10, 7 : 12}),
                      slot.Slot(4, {7 : 11, 8 : 13}),
                      slot.Slot(5, {2 : 0, 4 : 3, 8 : 12, 9 : 14}),
                      slot.Slot(6, {3 : 1, 7 : 8}),
                      slot.Slot(7, {4 : 2, 8 : 9}),
                      slot.Slot(8, {4 : 1, 7 : 6, }),
                      slot.Slot(9, {5 : 2, 8 : 7}),
                      slot.Slot(10, {6 : 3, 11 : 12}),
                      slot.Slot(11, {7 : 4, 12 : 13}),
                      slot.Slot(12, {11 : 10, 7 : 3, 8 : 5, 13 : 14}),
                      slot.Slot(13, {12 : 11, 8 : 4}),
                      slot.Slot(14, {13 : 12, 9 : 5})]

        # # Initializes total number of pegs to 15.
        self.total_pegs = self.get_total_pegs()
        #print(self.total_pegs, 'pegs remaining.')
        # Initializes the game board with a randomly selected empty slot.
        self.remove_first_peg()
        # Sets the initial board state.
        self.b_state = self.init_board_state()
        # Pushes start state onto the open stack.
        self.open.insert(0, self.get_board_state())
        # Appends the initial board state to the intermediate state list.
        self.i_states.append(self.get_board_state())

    # Generates the start state.
    def init_board_state(self):
        state = []
        for i in self.jumps:
            state.append(int(i.has_peg()))
        return state

    # Returns the current board state (node).
    def get_board_state(self):
        state = self.b_state
        for i in self.jumps:
            state[i.num] = (int(i.has_peg()))
        return tuple(state)

    # Removes the first peg from the board. Result is the root node.
    def remove_first_peg(self):
        first_peg = random.choice(self.jumps)
        first_peg.remove_peg()
        self.pegs.remove(first_peg.num)
        self.total_pegs -= 1
        print()
        print('Initial board state:')
        print('--------------------')
        for n in self.jumps:
            if n.num < 10:
                print('', str(n.num), ':', str(int(n.has_peg())))
            else:
                print(str(n.num), ':', str(int(n.has_peg())))
        print()
        print(self.total_pegs, 'pegs remaining.')
        print('The initial vacancy is at slot #', first_peg.num, '.', sep='')
        print()

    # Returns the total pegs currently on the board.
    def get_total_pegs(self):
        total = 0
        for i in self.jumps:
            if i.has_peg():
                total += 1
        return total
    
    # Executes a peg move.
    def make_move(self, move):
        source = self.jumps[move[0]]
        jumped = self.jumps[move[1]]
        destination = self.jumps[move[2]]
        source.remove_peg()
        self.pegs.remove(source.num)
        jumped.remove_peg()
        self.pegs.remove(jumped.num)
        self.total_pegs -= 1
        destination.add_peg()
        self.pegs.insert(0,destination.num)
        self.history.append(move)
        self.pegs.sort()

    # Backtracks to previous move.
    def backtrack(self):
        move = self.history.pop()
        source = self.jumps[move[0]]
        jumped = self.jumps[move[1]]
        destination = self.jumps[move[2]]
        self.pegs.sort()
        source.add_peg()
        self.pegs.insert(0,source.num)
        jumped.add_peg()
        self.pegs.insert(0,jumped.num)
        self.total_pegs += 1
        destination.remove_peg()
        self.pegs.remove(destination.num)
        self.pegs.sort()

    # Recursive Depth-First search algorithm (searches for a winning game board state).
    def DFS_solver(self):
        move_list = []
        if self.victory:
            return
        else:
            for i in self.jumps:
                for j in (i.move_opts(self.jumps)):
                    move_list.append(j)
            for i in move_list:
                self.make_move(i)
                if self.get_total_pegs() == 1:
                    print()
                    print('Peg jump history:')
                    print('--------------------')
                    print(self.history)
                    print()
                    print()
                    self.victory = True
                    print('Final board state:')
                    print('--------------------')
                    for n in self.jumps:
                        if n.num < 10:
                            print('', str(n.num), ':', str(int(n.has_peg())))
                        else:
                            print(str(n.num), ':', str(int(n.has_peg())))
                    print()
                    print(self.total_pegs, 'peg remaining.')
                    print('The last remaining peg is at slot #', *self.pegs, '.', sep='')
                    print()
                    print('Peg solitaire is solved!')
                    print()
                    print()
                    print()
                self.DFS_solver()
                self.backtrack()