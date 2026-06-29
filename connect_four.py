from colorama import Fore,Style,init
import random 

class MinimaxBot:
    def __init__(self, bot='Z', human='O', depth=5):
        self.bot = bot          # bot piece
        self.human = human      # human piece
        self.depth = depth

    # Get valid columns
    def valid_moves(self, board_obj):
        return [c for c in range(1, 8) if board_obj.avalible(c)]

    # Clone + simulate insertion
    def simulate(self, board_obj, col, piece):
        fake = board_obj.clone()
        if piece == self.bot:
            fake.insert(col, "bot")
        else:
            fake.insert(col, "p1")
        return fake

    # Score a window of 4 cells
    def evaluate_window(self, window):
        score = 0
        bot = self.bot
        opp = self.human

        # Bot winning patterns
        if window.count(bot) == 4:
            score += 10000
        elif window.count(bot) == 3 and window.count(' ') == 1:
            score += 100
        elif window.count(bot) == 2 and window.count(' ') == 2:
            score += 10

        # Opponent threats
        if window.count(opp) == 3 and window.count(' ') == 1:
            score -= 120

        return score

    # Complete evaluation of board state
    def score(self, board_obj):
        b = board_obj.board
        score = 0

        # Center column preference
        center_col = [b[r][3] for r in range(6)]
        score += center_col.count(self.bot) * 8

        # Score horizontal windows
        for r in range(6):
            for c in range(4):
                window = [b[r][c+i] for i in range(4)]
                score += self.evaluate_window(window)

        # Score vertical windows
        for c in range(7):
            for r in range(3):
                window = [b[r+i][c] for i in range(4)]
                score += self.evaluate_window(window)

        # Score \ diagonals
        for r in range(3):
            for c in range(4):
                window = [b[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window)

        # Score / diagonals
        for r in range(3, 6):
            for c in range(4):
                window = [b[r-i][c+i] for i in range(4)]
                score += self.evaluate_window(window)

        return score

    # Terminal check
    def is_terminal(self, board_obj):
        return board_obj.result() != False or board_obj.Tie()

    # Minimax with alpha-beta
    def minimax(self, board_obj, depth, alpha, beta, maximizing):
        winner = board_obj.result()

        # Terminal or depth-0 → return evaluation
        if depth == 0 or winner != False or board_obj.Tie():
            if winner == self.bot:
                return (1000000, None)
            elif winner == self.human:
                return (-1000000, None)
            else:
                return (self.score(board_obj), None)

        valid_cols = self.valid_moves(board_obj)

        if maximizing:
            value = -float("inf")
            best_col = random.choice(valid_cols)

            for col in valid_cols:
                sim = self.simulate(board_obj, col, self.bot)
                new_score, _ = self.minimax(sim, depth-1, alpha, beta, False)

                if new_score > value:
                    value = new_score
                    best_col = col

                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return value, best_col

        else:
            value = float("inf")
            best_col = random.choice(valid_cols)

            for col in valid_cols:
                sim = self.simulate(board_obj, col, self.human)
                new_score, _ = self.minimax(sim, depth-1, alpha, beta, True)

                if new_score < value:
                    value = new_score
                    best_col = col

                beta = min(beta, value)
                if alpha >= beta:
                    break

            return value, best_col

    # Public method to choose best move
    def choose(self, board_obj):
        _, best_move = self.minimax(board_obj, self.depth, -float("inf"), float("inf"), True)
        return best_move


class Board:
    def __init__(self):
        self.board = []

    def new(self):
        self.board = [[' ',' ',' ',' ',' ',' ',' '] for i in range(6)]
    
    def __str__(self):
        pt_board = self.colour()
        pro = ''
        pro += (Fore.BLACK + '='*9 + Style.RESET_ALL) + (' CONNECT-4 ') + (Fore.BLACK + '='*9+'\n' + Style.RESET_ALL)
        pro += (Fore.WHITE + '  1   2   3   4   5   6   7  \n' + Style.RESET_ALL)
        pro += (Fore.BLUE + '-'*29+'\n' + Style.RESET_ALL)

        for i in range(len(self.board)):
            if i != len(self.board)-1:
                pro += (Fore.BLUE + '| ' + Style.RESET_ALL) + (Fore.BLUE + ' | ' + Style.RESET_ALL).join(pt_board[i]) + Fore.BLUE + ' |' + Style.RESET_ALL + '\n'
                pro += (Fore.BLUE + '+---+---+---+---+---+---+---+\n' + Style.RESET_ALL)
            else:
                pro += (Fore.BLUE + '| ' + Style.RESET_ALL) + (Fore.BLUE + ' | ' + Style.RESET_ALL).join(pt_board[i]) + Fore.BLUE + ' |' + Style.RESET_ALL + '\n'
                pro += (Fore.BLUE + '-'*29 + Style.RESET_ALL)

        return pro
    
    def avalible(self,column):
        st = ''
        for row in self.board:
            st += row[column-1]
        
        if ' ' not in st:
            return False
        else:
            return True
        
    def insert(self,column,pla):
        if self.avalible(column):
            st = ''
            for row in self.board:
                st += row[column-1]

            row =  st[::-1].find(' ')
            out_row = 5-row
            
            #insert coin
            #Idea pl1(red) pl2,bot(yellow) , Code = [O(pl1),X(pl2),Z(bot)]
            d = {'p1':'O','p2':'X','bot':'Z'}
            self.board[out_row][column-1] = d[pla]
            return True
        
        else:
            return False
 
    def win(self,string):
        for win in  ['OOOO','XXXX','ZZZZ']:
            if win in string:
                return True
            
    def result(self):
        #True = win
        #Check for horizontal win
        for row in self.board:
            s = ''.join(row)
            for win in ['OOOO','XXXX','ZZZZ']:
                if win in s:
                    return win[0]
                
        #Check for vertical win
        for column in range(7):
            s = ''
            for i in range(6):
                s += self.board[i][column]
            
            for win in ['OOOO','XXXX','ZZZZ']:
                if win in s:
                    return win[0]
                
        #Check /
        for down in range(3):
            for side in range(4):
                s = self.board[down+3][side] +  self.board[down+2][side+1] +  self.board[down+1][side+2] +  self.board[down][side+3]
                if self.win(s) == True:
                    return s[0]
        #Check \
        for down in range(3):
            for side in range(4):
                s = self.board[down][side] +  self.board[down+1][side+1] +  self.board[down+2][side+2] +  self.board[down+3][side+3]
                if self.win(s) == True:
                    return s[0]
                
        return False

    def colour(self):
        pt_board = []
        for line in self.board:
            decoy = []
            for item in line:
                if item == ' ':
                    decoy.append(' ')
                elif item == 'O':
                    decoy.append(Fore.YELLOW + 'O' + Style.RESET_ALL)
                elif item == 'X' or item == 'Z':
                    decoy.append(Fore.RED + 'O' + Style.RESET_ALL)
            pt_board.append(decoy)

        return pt_board
    
    def Tie(self):
        if self.result() != False:
            return False
        
        s = ''
        for line in self.board:
            for item in line:
                s += item
        
        if ' ' in s:
            return False
        else:
            return True

    def clone(self):
        new_board = Board()
        new_board.board = [row[:] for row in self.board]        
        return new_board

class Player:
    def __init__(self,name):
        self.name = name

    def input(self):
        ans = ''
        while ans not in range(1,8):
            try:
                ans = int(input('Enter drop index: '))
                if ans not in range(1,8):
                    print('Invalid index')
            except:
                print('Invalid index')

        return ans


print('='*29)
###Output start
while True:
    start = input('Press enter to start: ')
    if start == '':
        break

print('='*29)
print("Select Game Mode:")
print("  1) Single Player ")
print("  2) Multiplayer")

while True:
    try:
        mode = int(input("Enter 1 or 2: ").strip())
        if mode in [1,2]:
            print('='*29)
            break
        else:
            print('Invalid game mode...')
    except:
        print('Invalid game mode...')

Play = True
count = 0
con = False
while Play:
    #Ask
    if count != 0:
        while True:
            ask = input('Continue(yes/no): ')
            if ask in ['yes','no']:
                break
    
        if ask == 'yes':
            con = True
        else:
            con = False
            Play = False
            print('Shuting down...')
            print('============ END ============')
            break

    count += 1

    #make board
    board = Board()
    board.new()

    if con == False:
        #Make player objects
        if mode == 1:
            per1 = input('Enter name: ')
            p1 = Player(per1)
            ####
            bot = MinimaxBot(bot="Z", human="O", depth=5)
            p2 = "bot"

        elif mode == 2:
            per1 = input('Enter name of P1: ')
            p1 = Player(per1)
            per2 = input('Enter name of P2: ')
            p2 = Player(per2)

    over = False
    while not over:
        #check for tie
        if board.Tie() == True:
            print('Tie game!')
            break
        #Show board
        print(board)

        #ask for turn -> can you put it there? -> if can. Put there -> check if win or not -> go to p2
        #ask for turn player1
        turn1 = p1.input()

        #avalable?
        if board.avalible(turn1):
            #insert coin
            board.insert(turn1,'p1')

            #check for win
            if board.result() == 'O':
                print(board)
                print(f'{p1.name} wins!')
                print('='*29)
                break

        else:
            while not board.avalible(turn1):
                print('Column is full...')
                turn1 = p1.input()
            
            #insert coin
            board.insert(turn1,'p1')

            #check for win
            if board.result() == 'O':
                print(board)
                print(f'{p1.name} wins!')
                print('='*29)
                break

        #Show board after turn1
        print(board)

        #player2 if/else for bot
        if mode == 1:
            print("Bot thinking...")

            turn2 = bot.choose(board)   # Minimax chooses column
            board.insert(turn2, 'bot')

            print(board)

            if board.result() == 'Z':
                print("Bot wins!")
                print('='*29)
                break

            turn = 1
            continue

        elif mode == 2:
            #ask for player2 turn
            turn2 = p2.input()
            
            #avalable?
            if board.avalible(turn2):
                #insert coin
                board.insert(turn2,'p2')

                #check for win
                if board.result() == 'X':
                    print(board)
                    print(f'{p2.name} wins!')
                    print('='*29)
                    break

            else:
                while not board.avalible(turn2):
                    print('Column is full...')
                    turn2 = p2.input()

                #insert coin
                board.insert(turn2,'p2')

                #check for win
                if board.result() == 'X':
                    print(board)
                    print(f'{p2.name} wins!')
                    print('='*29)
                    break
 