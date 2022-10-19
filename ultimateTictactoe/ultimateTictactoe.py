
# If a move is played so that it is to win a local board by the rules of normal tic-tac-toe, then the entire local board is marked as a victory for the player in the global board.
# Once a local board is won by a player or it is filled completely, no more moves may be played in that board.
# If a player is sent to such a board, then that player may play in any other board.
# Game play ends when either a player wins the global board or there are no legal moves remaining, in which case the game is a draw.[3]

# 每个3x3的grid如果连成一条后就不能再放，总体9x9赢的规则也是，比如3x3小grid被X连成一条了，整个区块就标为X，最后一样检查9x9大matrix是否连成一条线(row, col, diag)。

# 1. toggle X/0 t‍‌‍‌‌‍‌‍‍‌‍‌‌‌‌‍‌‍‌‌urns
# 2. 算接下来的落点，检查该点可否放
# 3. 放完检查是否赢(小grid 3x3)
# 4. 放完检查是否赢(大grid 9x9)
# 5. 如果都没赢往前持续loop，当9x9都走满的时候，还要检查最终结果是否break ties（木有人赢）


class TicTacToeBoard:
    """General board class. Extended by GlobalBoard and LocalBoard"""

    def __init__(self) -> None:
        # 3x3 grid of zeros. Will be set to 1 or 2 when the square is claimed
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def checkCol(self, col, player):
        for row in range(3):
            if self.board[row][col] != player:
                return False
        return True

    def checkRow(self, row, player):
        for col in range(3):
            if self.board[row][col] != player:
                return False
        return True

    def checkDiagonal(self, player):
        for row in range(3):
            if self.board[row][row] != player:
                return False
        return True

    def checkAntiDiagonal(self, player):
        for row in range(3):
            if self.board[row][3 - row - 1] != player:
                return False
        return True


"""******************************************************************************************************************"""


class LocalBoard(TicTacToeBoard):
    def __init__(self, index):
        TicTacToeBoard.__init__(self)
        # self.playable: bool = True
        self.index: int = index


"""******************************************************************************************************************"""


class GlobalBoard(TicTacToeBoard):
    def __init__(self):
        TicTacToeBoard.__init__(self)
        # a list of 9 local board
        self.local_board_list = [LocalBoard(i) for i in range(9)]

    def print_board(self):
        """Prints the board in the command line"""
        print()
        print('-' * 35)
        print()

        # each loop prints a row of the local boards
        for x in range(3):
            print(self.local_board_list[0].board[x], '\t', self.local_board_list[1].board[x], '\t',
                  self.local_board_list[2].board[x])
        print()
        for x in range(3):
            print(self.local_board_list[3].board[x], '\t', self.local_board_list[4].board[x], '\t',
                  self.local_board_list[5].board[x])
        print()
        for x in range(3):
            print(self.local_board_list[6].board[x], '\t', self.local_board_list[7].board[x], '\t',
                  self.local_board_list[8].board[x])

    # 2. 算接下来的落点，检查该点可否放
    def isValid(self, row, col, index):
        # first check if that board is playable
        x = index // 3
        y = index % 3
        if self.board[x][y] != ' ':
            return False

        # first check if that point is already occupied
        if self.local_board_list[index].board[row][col] != ' ':
            return False

        # else it is a valid point
        return True

    # 3. 放
    def makeMove(self, row, col, index, player):
        self.local_board_list[index].board[row][col] = player
        # if small grid won, update my board with the player_id
        if self.hasSmallGridWon(row, col, index, player):
            x = index // 3
            y = index % 3
            self.board[x][y] = player

    # 4. 放完检查是否赢(小grid 3x3)
    def hasSmallGridWon(self, row, col, index, player):
        if self.local_board_list[index].checkCol(col, player) or \
                self.local_board_list[index].checkRow(row, player) or \
            (row == col and self.local_board_list[index].checkDiagonal(player)) or \
                (row == (3 - col - 1) and self.local_board_list[index].checkAntiDiagonal(player)):
            return True

        # else it is not winning
        return False

     # 5. 放完检查是否赢(大grid 3x3)
    def hasBigGridWon(self, row, col, player):
        if self.checkCol(col, player) or \
                self.checkRow(row, player) or \
            (row == col and self.checkDiagonal(player)) or \
                (row == (3 - col - 1) and self.checkAntiDiagonal(player)):
            return True
        # else it is not winning
        return False


globalBoard = GlobalBoard()

board_num = int(input("which board do you want to place (0 - 8): "))
cur_player = 'X'
while True:
    row = int(input("what row? "))
    col = int(input("what col? "))
    if globalBoard.isValid(row, col, board_num):
        globalBoard.makeMove(row, col, board_num, cur_player)

    for i in range(3):
        for j in range(3):
            if globalBoard.hasBigGridWon(i, j, cur_player):
                print('game over')
                break

    # 1. toggle X/0 t‍‌‍‌‌‍‌‍‍‌‍‌‌‌‌‍‌‍‌‌urns
    if cur_player == 'X':
        cur_player = 'O'
    else:
        cur_player = 'X'
