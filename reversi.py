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
        self.board = [[' ' for _ in range(BOARD_COLS)]
                      for _ in range(BOARD_ROWS)]

        self.board[int((BOARD_ROWS/2) - 1)][int((BOARD_COLS/2) - 1)] = 'B'
        self.board[int(BOARD_ROWS/2)][int(BOARD_COLS/2)] = 'B'
        self.board[int((BOARD_ROWS/2) - 1)][int(BOARD_COLS/2)] = 'W'
        self.board[int(BOARD_ROWS/2)][int((BOARD_COLS/2) - 1)] = 'W'

        self.cur_turn = 'B'
        self.opposite_turn = 'W'

        self.position_to_flip = []

        self.winner = ''

    def print_board(self):
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
        return self.cur_turn

    def is_valid_row(self, inputRow):
        return 0 <= inputRow < BOARD_ROWS

    def is_valid_col(self, inputCol):
        return 0 <= inputCol < BOARD_COLS

    def is_valid_move(self, inputRow, inputCol):

        # check if there is an element already occupied or the input row and col are out of bound
        if self.board[inputRow][inputCol] != ' ' or not self.is_valid_row(inputRow) or not self.is_valid_col(inputCol):
            return False

        for dirX, dirY in MOVE_DIRS:
            newRow = inputRow + dirX
            newCol = inputCol + dirY

            # check if current location is in-bound and is located at the opposite_turn
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

        # if None position to flip, return False
        if len(self.position_to_flip) == 0:
            return False
        else:
            return True

    def make_move(self, inputRow, inputCol):

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

    def is_game_over(self):
        position_to_flip = []

        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLS):
                if self.is_valid_move(row, column) != False:
                    position_to_flip.append([row, column])

        if len(position_to_flip) == 0:
            self.change_turn()
            for row in range(BOARD_ROWS):
                for column in range(BOARD_COLS):
                    if self.is_valid_move(row, col) != False:
                        position_to_flip.append([row, column])
            return len(position_to_flip) == 0
        return False


game = Reversi()
game_over = False

while game_over == False:
    game.print_board()
    print()
    game.print_score()
    print('It is now ', game.print_turn(), ' turn')

    row = int(input("what is the row you want to enter? "))
    col = int(input("what is the col you want to enter? "))

    while game.is_valid_move(row, col) == False:
        print("Invalid user move! Reenter the row and col!")
        print('It is now ', game.print_turn(), ' turn')

        row = int(input("what is the row you want to enter? "))
        col = int(input("what is the col you want to enter? "))

    game.make_move(row, col)
    if game.is_game_over():
        break

    game.change_turn()
    game.reset_position_to_flip()
