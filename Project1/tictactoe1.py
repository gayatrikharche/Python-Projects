from IPython.display import clear_output
import random

def display_board(board):
    clear_output() 
    
    print("┌───┬───┬───┐")
    print(f"│ {board[7]} │ {board[8]} │ {board[9]} │")
    print("├───┼───┼───┤")
    print(f"│ {board[4]} │ {board[5]} │ {board[6]} │")
    print("├───┼───┼───┤")
    print(f"│ {board[1]} │ {board[2]} │ {board[3]} │")
    print("└───┴───┴───┘")
    
def player_input():
    while True:
        marker = input("Player 1: Do you want to be X or O? ").strip().upper()
        if marker in ("X", "O"):
            return (marker, "O" if marker == "X" else "X")
        else:
            print("Invalid choice!")
            
def place_marker(board, marker, position):
    board[position] = marker
    
def win_check(board, mark):
    winning_lines = [
        (7, 8, 9),
        (4, 5, 6),  
        (1, 2, 3), 
        (7, 4, 1),  
        (8, 5, 2),  
        (9, 6, 3),  
        (7, 5, 3),  
        (9, 5, 1), 
    ]
    return any(board[a] == board[b] == board[c] == mark for a, b, c in winning_lines)

def choose_first():
    rand_no = random.randint(0,1)
    if rand_no == 0:
        return 'Player 2'
    else:
        return 'Player 1'
    
def space_check(board, position):
    if board[position] == ' ':
        return True
    else:
        return False
    
def full_board_check(board):
    for i in range(1,10):
        if space_check(board, i):
            return False
    return True

def player_choice(board):
    selected_pos = 0
    
    while selected_pos not in [1,2,3,4,5,6,7,8,9] or not space_check(board, selected_pos):
        selected_pos = int(input('Choose your next position: (1-9) '))
        
    return selected_pos

def replay():
    return input('Do you want to play again? Enter Yes or No: ').lower().startswith('y')

print("Tic Tac Toe Game")

while True:
     board = [' ']*10
     player1, player2 = player_input()
     current = choose_first()
     print(f"It is {current}'s turn")
     game= input("Ready to play? Enter Yes or No :")
     if game.lower()[0]=='y':
         game = True
     else:
         game=False
     while game:
        if current=='Player 1':
            print("It is Player 1's turn")
            display_board(board)
            choice = player_choice(board)
            place_marker(board, player1, choice)
            if win_check(board, player1):
                display_board(board)
                print("Congratulations! Player 1 won the game!")
                game = False
            else:
                if full_board_check(board):
                    print("It is a draw!")
                    break
                else:
                    current = 'Player 2'
        else:
            display_board(board)
            print("It is Player 2's turn")
            choice = player_choice(board)
            place_marker(board, player2, choice)
            if win_check(board, player2):
                display_board(board)
                print("Congratulations! Player 2 won the game!")
                game = False
            else:
                if full_board_check(board):
                    print("It is a draw!")
                    break
                else:
                    current = 'Player 1'
                    
     if not replay():
        break

