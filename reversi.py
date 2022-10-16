# Hard-coded board size
BOARD_ROWS = 8
BOARD_COLS = 8


# Define all the possible directions in which a player's move can flip
# their adversary's tiles as constant (0 – the current row/column,
# +1 – the next row/column, -1 – the previous row/column)
MOVE_DIRS = [(-1, -1), (-1, 0), (-1, 1),
             (0, -1),           (0, 1),
             (1, -1), (1, 0),  (1, 1)]


class Reversi():
    def __init__(self):
        '''
            Initialize the board:
            1. initialize the 4 positions in the center of the board
            2. initialize cur_turn to black
            3. initialize opposite_turn to white 
            4. initialize position to flip to empty list
        '''

        self.board = [[' ' for _ in range(BOARD_COLS)]
                      for _ in range(BOARD_ROWS)]

        self.board[int((BOARD_ROWS/2) - 1)][int((BOARD_COLS/2) - 1)] = 'B'
        self.board[int(BOARD_ROWS/2)][int(BOARD_COLS/2)] = 'B'
        self.board[int((BOARD_ROWS/2) - 1)][int(BOARD_COLS/2)] = 'W'
        self.board[int(BOARD_ROWS/2)][int((BOARD_COLS/2) - 1)] = 'W'

        self.cur_turn = 'B'
        self.opposite_turn = 'W'

        self.position_to_flip = []

    def print_board(self):
        '''
            Print the board
        '''

        print("    0   1   2   3   4   5   6   7")
        print("  +---+---+---+---+---+---+---+---+")
        c = 0
        for i in range(BOARD_ROWS):
            print(i, "| ", end="")
            for j in range(BOARD_COLS):
                c = self.board[i][j]
                if c == ' ':
                    print(" ", end="")
                elif c == 'B':
                    print("B", end="")
                else:
                    print("W", end="")
                print(" | ", end="")
            print(" ")
            print("  +---+---+---+---+---+---+---+---+")

    def print_score(self):
        '''
            Print the score of the board
        '''

        black_score = 0
        white_score = 0

        for row in self.board:
            for column in row:
                if column == 'B':
                    black_score += 1
                elif column == 'W':
                    white_score += 1
        print('game score is B: ' + str(black_score) +
              ' | ' + 'W: ' + str(white_score))

    def print_turn(self):
        '''
            Print whose turn it is now
        '''

        return self.cur_turn

    def is_valid_row(self, inputRow):
        '''
            Check if inputRow is within the board boundary
        '''

        return 0 <= inputRow < BOARD_ROWS

    def is_valid_col(self, inputCol):
        '''
            Check if inputCol is within the board boundary
        '''

        return 0 <= inputCol < BOARD_COLS

    def is_valid_move(self, inputRow, inputCol):
        '''
            Check if my current position is a valid move. 
            If so, modify the self.position_to_flip and return True
            If not, return False
        '''

        # check if the input row and col are out of bound or if there is an element already occupied (the order of check is really important here)
        if not self.is_valid_row(inputRow) or not self.is_valid_col(inputCol) or self.board[inputRow][inputCol] != ' ':
            # print('this is invalid')
            return False

        for dirX, dirY in MOVE_DIRS:
            newRow = inputRow + dirX
            newCol = inputCol + dirY

            # check if current location is in bound and is located at the opposite_turn
            if self.is_valid_row(newRow) and self.is_valid_col(newCol) and self.board[newRow][newCol] == self.opposite_turn:
                while self.board[newRow][newCol] == self.opposite_turn:
                    newRow += dirX
                    newCol += dirY

                    # if this position is not valid, break the whie loop
                    if not self.is_valid_row(newRow) or not self.is_valid_col(newCol):
                        break

                # if this positioon is not valid, continue to next MOVE_DIR
                if not self.is_valid_row(newRow) or not self.is_valid_col(newCol):
                    continue

                # now we have arrived the current_turn, we reverse the move
                if self.board[newRow][newCol] == self.cur_turn:

                    while True:
                        newRow -= dirX
                        newCol -= dirY

                        if (newRow, newCol) == (inputRow, inputCol):
                            break

                        # store the position to be flipped
                        self.position_to_flip.append([newRow, newCol])

        # if no position to flip, return False
        if len(self.position_to_flip) == 0:
            return False
        else:
            return True

    def make_move(self, inputRow, inputCol):
        '''
            place my current position on the board, while flipping all the positions between my initial position and my current position
        '''

        if self.is_valid_move(inputRow, inputCol):
            # make flip all the positions along the way
            for row, column in self.position_to_flip:
                self.board[row][column] = self.cur_turn
            # also add the inputRow and inputCol to the board
            self.board[inputRow][inputCol] = self.cur_turn

    def change_turn(self):
        '''
            Given the current player's turn, change to the opposing player's turn.
        '''
        if self.cur_turn == 'B':
            self.cur_turn = 'W'
            self.opposite_turn = 'B'
        else:
            self.cur_turn = 'B'
            self.opposite_turn = 'W'

    def reset_position_to_flip(self):
        '''
            reset position to flip.
        '''
        self.position_to_flip = []

    def is_moveable(self):
        '''
            check if current turn is movable
        '''

        moveable = []

        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLS):
                if self.is_valid_move(row, column) != False:
                    # because is_valid_move will modify the position_to_flip
                    self.position_to_flip = []
                    moveable.append([row, column])

        print('movabale is for ', self.cur_turn, ' is ', moveable)
        return len(moveable) != 0

    def get_winner(self):
        '''
            get the winner of the game
        '''

        black_score = 0
        white_score = 0

        for row in self.board:
            for column in row:
                if column == 'B':
                    black_score += 1
                elif column == 'W':
                    white_score += 1
        if black_score > white_score:
            return 'black'
        elif black_score < white_score:
            return 'white'
        else:
            return 'draw'


game = Reversi()
game_over = False

while game_over == False:
    game.print_board()
    print()
    game.print_score()
    print('It is now ', game.print_turn(), ' turn')

    if not game.is_moveable():
        print(game.print_turn(), ' cannot move, so switch turn')
        game.change_turn()
        if not game.is_moveable():
            print(game.print_turn(), ' cannot move either,so game is over')
            game.print_score()
            print('winner is ', game.get_winner())
            break

    row = int(input("what is the row you want to enter? "))
    col = int(input("what is the col you want to enter? "))

    while game.is_valid_move(row, col) == False:

        print("Invalid user move! Reenter the row and col!")
        print('It is now ', game.print_turn(), ' turn')

        row = int(input("what is the row you want to enter? "))
        col = int(input("what is the col you want to enter? "))

    game.make_move(row, col)
    game.change_turn()
    game.reset_position_to_flip()
