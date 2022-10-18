from enum import Enum
 
class Piece(Enum):
    EMPTY = 0
    X = 1
    O = 2


class Square:
    def __init__(self, piece=Piece.EMPTY, timer=-1):
        self.piece = piece
        self.timer = timer

class Coordinate:
    def __init__(self, col, row):
        self.col = col
        self.row = row
    
class Game:
    def __init__(self, size):
        self.size = size
        self.board = [[Square() for _ in range(size)]
                      for _ in range(size)]
        self.cur_player = Piece.X
        
    def getUserMove(self):
        col = int(input("what is the col you want to enter? "))
        row = int(input("what is the row you want to enter? "))
        return Coordinate(col, row)
    
    def render(self):
        print("    a  b  c  d  e  f  g  h  i")
        print("    o  o  o  o  o  o  o  o  o")
        print("    --------------------------")
        
        for y in range(self.size):
            line = ""
            line += str(y + 1)
            line += ' x|'
            for x in range(self.size):
                square = self.board[x][y]
                if square.piece == Piece.O:
                    line += 'O'

                elif square.piece == Piece.X:
                    line += 'X'

                elif square.piece == Piece.EMPTY:
                    line += ' '

                if square.timer >= 0:
                    line += str(square.timer)
                else:
                    line += ' '
                
                line += '|'
                
            line += 'x'
            print(line)
            print("    --------------------------")
        print("    o  o  o  o  o  o  o  o  o")
    
    def changeTurn(self):
        if self.cur_player == Piece.X:
            self.cur_player = Piece.O
        else:
            self.cur_player = Piece.X
    
    def defuseNeighborBombs(self, prev_player, x, y):
        #defuse neighbor bombs belonging to the same player(set their timers to a negative value)
        
        Dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        
        #find if it has neighbors around it. If not, return 4
        def hasNeighbors():
            res = False
            for Dir in Dirs:
                newX = x + Dir[0]
                newY = y + Dir[1]
                if newX >= 0 and newX < 9 and newY >= 0 and newY < 9 and self.board[newX][newY].piece == prev_player:
                    res = True
                    break
            return res
        
        #if it has neighbor, call dfs to make its neighbor's time all -1
        def dfs(x, y):
            self.board[x][y].timer = -1
            for Dir in Dirs:
                newX = x + Dir[0]
                newY = y + Dir[1]
                if newX >= 0 and newX < 9 and newY >= 0 and newY < 9 and self.board[newX][newY].piece == prev_player:
                    dfs(newX, newY)
        
        
        if hasNeighbors():
            dfs(x, y)
        else:
            self.board[x][y].timer = 4
            return
    
    def decrementBombCounter(self,x, y):
        #decrement all other bomb's counter by 1 (unless its timer is -1 or it is itself )
        for i in range(9):
            for j in range(9):
                if self.board[i][j].timer == -1 or (i == x and j == y):
                    continue
                else:
                    self.board[i][j].timer -= 1
        
    
    def play(self):
        while True:
            self.render()
            coordinate = self.getUserMove()
            
            #Todo:  Do not accept invalid moves (Done)
            while coordinate.col < 0 or coordinate.col >= 9 or coordinate.row < 0 or coordinate.row >= 9: 
                print("invalid. re-enter move")
                coordinate = self.getUserMove()
            print("move is valid now")
            
            #Todo: Alternate player (Done)
            prev_player = self.cur_player
            self.changeTurn()
            
            #Todo: defuse neighbor bombs belonging to the same player(set their timers to a negative value)
            self.defuseNeighborBombs(prev_player, coordinate.col, coordinate.row)
            
            #Todo: decrement all other bomb's counter by 1 (unless its timer is -1 and itself )
            self.decrementBombCounter(coordinate.col, coordinate.row)
            
            #Todo: explode any bombs where the timer has reached zero
            
            #Todo: Convert any lonely claimed squares to bombs with timer set to 4
            
            #Todo: Check if the current player won by making a spanning bridge
            
            #Todo: if there are no empty squares left on the board, this player is the winner
            
            
    
game = Game(9)
game.play()
    
    
    