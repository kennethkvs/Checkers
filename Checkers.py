class CheckersGame () :
    def __init__ (self) :
        self.board = [ [0, 2, 0, 2, 0, 2, 0, 2]
                     , [2, 0, 2, 0, 2, 0, 2, 0]
                     , [0, 2, 0, 2, 0, 2, 0, 2]
                     , [0, 0, 0, 0, 0, 0, 0, 0]
                     , [0, 0, 0, 0, 0, 0, 0, 0]
                     , [1, 0, 1, 0, 1, 0, 1, 0]
                     , [0, 1, 0, 1, 0, 1, 0, 1]
                     , [1, 0, 1, 0, 1, 0, 1, 0]
                     ]
        self.whoseMove = 'white'
        self.isWon = 0
    
    def checkWinner(self) :
        whiteCount = 0
        redCount = 0
        for i in range(len(self.board)):
            for j in self.board[i]:
                if j == 1 or j == 3:
                    whiteCount += 1
                elif j == 2 or j == 4:
                    redCount += 1
        if whiteCount > 0 and redCount == 0:
            self.isWon = 'white'
        elif redCount > 0 and whiteCount == 0:
            self.isWon = 'red'
    
    def changeTurn(self) :
        if self.whoseMove == 'white':
            self.whoseMove = 'red'
        elif self.whoseMove == 'red':
            self.whoseMove = 'white'
    
    def parseMove (self, move) :
        try:
            move = move.split(' ')
        except:
            raise ValueError
        if len(move) < 2:
            raise ValueError
        for i in move:
            if len(i) != 2:
                raise ValueError
            elif int(i[0]) > 7 or int(i[0]) < 0 or int(i[1]) > 7 or int(i[1]) < 0:
                raise ValueError
        coords = []
        for i in move:
            coords.append((int(i[0]), int(i[1])))
        return tuple(coords)
    
    def move(self, move) :
        move = self.parseMove(move)
        #Update Board
        for i in range(1,len(move)):
            self.board[move[i][0]][move[i][1]] = self.board[move[i-1][0]][move[i-1][1]]
            self.board[move[i-1][0]][move[i-1][1]] = 0
            if self.whoseMove == 'white':
                midpoint = self.board[(move[i][0]+move[i-1][0])//2][(move[i][1]+move[i-1][1])//2]
                if midpoint == 2 or midpoint == 4:
                    self.board[(move[i][0]+move[i-1][0])//2][(move[i][1]+move[i-1][1])//2] = 0
            elif self.whoseMove == 'red':
                midpoint = self.board[(move[i][0]+move[i-1][0])//2][(move[i][1]+move[i-1][1])//2]
                if midpoint == 1 or midpoint == 3:
                    self.board[(move[i][0]+move[i-1][0])//2][(move[i][1]+move[i-1][1])//2] = 0
            else:
                print("Invalid Move")

        #Change to King
        for i in range(len(self.board[0])):
            if self.board[0][i] == 1:
                self.board[0][i] = 3

        for j in range(len(self.board[7])):
            if self.board[7][j] == 2:
                self.board[7][j] = 4
                
        self.changeTurn()
        self.checkWinner()
        
    def isValidMove(self, move):
        move = self.parseMove(move)
        checker = self.board[move[0][0]][move[0][1]]
        if self.isWon != 0:
            return False
        if checker == 0:
            return False
        if self.whoseMove == 'red' and (checker == 1 or checker == 3):
            return False
        if self.whoseMove == 'white' and (checker == 2 or checker == 4):
            return False
        
        for i in range(1,len(move)):
            posY = move[i-1][0]
            posX = move[i-1][1]
            moveY = move[i][0]
            moveX = move[i][1]
            
            #Check if white move up, if red move down (not king)
            if checker == 1:
                if posY < moveY :
                    return False
            elif checker == 2:
                if posY > moveY :
                    return False
            
            #Merry GO AROUND... + Check if it's empty
            if not((checker == 3 or checker == 4) and move[0][0] == move[i][0] and move[0][1] == move[i][1]) and self.board[moveY][moveX] != 0:
                return False
            
            #Checkers can't move to white spaces ever -> White spaces have even coordinate sums.
            if (moveY + moveX) % 2 == 0:
                return False
            
            #You go ONLY where you can go Checkers
            midpoint = self.board[(posY+moveY)//2][(posX+moveX)//2] 
            if self.whoseMove == 'white' and (midpoint == 2 or midpoint == 4):
                moveTo = [(posY+1, posX+1), (posY-1, posX+1), (posY+1, posX-1), (posY-1, posX-1),
                          (posY+2, posX+2), (posY-2, posX+2), (posY+2, posX-2), (posY-2, posX-2)]
            elif self.whoseMove == 'red' and (midpoint == 1 or midpoint == 3):
                moveTo = [(posY+1, posX+1), (posY-1, posX+1), (posY+1, posX-1), (posY-1, posX-1),
                          (posY+2, posX+2), (posY-2, posX+2), (posY+2, posX-2), (posY-2, posX-2)]
            else:
                moveTo = [(posY+1, posX+1), (posY-1, posX+1), (posY+1, posX-1), (posY-1, posX-1)]
            
            if (moveY, moveX) not in moveTo:
                return False
            
        return True

# Functions to run the game       
    def __str__ (self) :
        out = "  0 1 2 3 4 5 6 7 \n ╔═╤═╤═╤═╤═╤═╤═╤═╗\n"
        i = 0
        for row in self.board :
            out += f"{str(i)}║"
            j = 0
            for item in row :
                if item == 0:
                    out += "░" if (i + j) % 2 == 0 else " "
                elif item >= 1 and item <= 4:
                    out += ["○", "●", "♔", "♚"][item-1]
                out += "│"
                j += 1
            out = out[:-1]
            out += f"║{str(i)}\n ╟─┼─┼─┼─┼─┼─┼─┼─╢\n"
            i += 1
        out = out[:-18]
        out += "╚═╧═╧═╧═╧═╧═╧═╧═╝\n  0 1 2 3 4 5 6 7 \n"
        return out
    
def runGame (init = False, moveList = False) :
    game = CheckersGame()

    if (init != False) :
        game.board = init
    
    print("Checkers Initialized...")
    print(game)
    if (moveList != False) :
        print("Move List Detected, executing moves")
        for move in moveList :
            print(f"{game.whoseMove} makes move {move}\n")
            if (move == "q") :
                return
            if (game.isValidMove(move)) :
                game.move(move)
                print(game)
                if (game.isWon != 0) :
                    break
            else :
                print("Invalid Move")    
                
    print("Moves must be typed as coordinates (with no commas or brackets) separated by spaces. Row, then column.")
    print("Example: 54 43")
    print("When performing multiple jumps, enter each co-ordinate your piece will land on in sequence.")
    while (game.isWon == False) :
        print(f"{game.whoseMove} to move")
        move = input(">> ")
        if (move == "q") :
            return
        if (game.isValidMove(move)) :
            game.move(move)
            print(game)
            if (game.isWon != 0) :
                break
        else :
            print("Invalid Move")
    print("The Game is Finished!")
    print(f"Congratulations, {game.isWon}!")