import chess
import sys
import copy 
import math

# import chess by using PIP 
# pip install python-chess

def switchlocation(string):
    return string[2:4] + string[0:2]

# alpha beta move
def alphaBetaMax(board,alpha,beta,depthleft,AI,repeat_move):
    bestmove = None

    # Define all the available move_list in the function
    if(check_must_eat(board) == []):
        move_list = []
        moves = board.legal_moves
        for move in moves:
            move_list.append(move)
    else:
        move_list = check_must_eat(board)

    # Change the move to str
    str_move_list = []
    for moves in move_list:
        str_move_list.append(str(moves))

    if(repeat_move != None):
        if switchlocation(repeat_move) in str_move_list:
            str_move_list.remove(switchlocation(repeat_move))
        if repeat_move in str_move_list:
            str_move_list.remove(repeat_move)

    # End of Node
    if (depthleft == 0 or str_move_list == [] or board.is_game_over()):
        return (eval_board_value(board,AI),None)

    for moves in str_move_list:
        if moves not in legal_move(board):
            str_move_list.remove(str(moves))
    
    if(str_move_list == []):
          return (eval_board_value(board,AI),None)
    else:
        # loop to Evaluate the Value
        for moves in str_move_list:
            # Copy the board for the next move
            temp_board = copy.deepcopy(board)
            temp_board.push_uci(moves)

        # Calculate the value of the child
            score, move = alphaBetaMin(temp_board,alpha,beta,depthleft-1,AI,repeat_move);

            if(score > alpha):
                alpha = score
                bestmove = moves
                if(score >= beta):
                    #cut off
                    break

    return (alpha, bestmove)

def alphaBetaMin(board,alpha,beta,depthleft,AI,repeat_move):

    # Define all the available move_list in the function
    if(check_must_eat(board) == []):
        # Define all the available move_list in the function
        move_list = []
        moves = board.legal_moves
        for move in moves:
            move_list.append(move)
    else:
        move_list = check_must_eat(board)
    
    bestmove = None

    #Convert move to str
    str_move_list = []
    for moves in move_list:
        str_move_list.append(str(moves))

    if(repeat_move != None):
        if switchlocation(repeat_move) in str_move_list :
            str_move_list.remove(switchlocation(repeat_move))

        if repeat_move in str_move_list:
            str_move_list.remove(repeat_move)

    if (depthleft == 0 or str_move_list == []or board.is_game_over()):
        return (-1*eval_board_value(board,AI),None)

    for moves in str_move_list:
        if moves not in legal_move(board):
            str_move_list.remove(str(moves))

    if(str_move_list == []):
         return (eval_board_value(board,AI),None)
    else:
        # loop to Evaluate the Value in all moves
        for moves in str_move_list:
            # Copy the board for the next move
            temp_board = copy.deepcopy(board)
            temp_board.push_uci(moves)

            score, move = alphaBetaMax(temp_board,alpha,beta,depthleft-1,AI,repeat_move);

            if(score < beta):
                beta = score
                bestmove = moves
                if(score <= alpha):
                     #cut off
                    break
    return (beta,bestmove)

# evaluate function
def eval_board_value(board,AI):
    list_of_pieces = []
    board_value = 0;
    for location in range(64):
        # Get the pieces at the current location
        if(board.piece_at(location) != None):
            list_of_pieces.append(board.piece_at(location).symbol())

    list_move = board.pseudo_legal_moves
    number_move_black = 0
    number_move_white = 0

    check_value = 0;

    for move in list_move:
        temp_board = copy.deepcopy(board)
        temp_board.push(move)
        if (board.turn == True):
            number_move_white += 1
            if(temp_board.is_checkmate()):
                check_value = 100
        else:
            number_move_black += 1
            if(temp_board.is_checkmate()):
                check_value = 100


    board.push_uci('0000')

    list_move = board.legal_moves

    for move in list_move:
        temp_board = copy.deepcopy(board)
        temp_board.push(move)
        if (board.turn == True):
            number_move_white += 1
            if(temp_board.is_checkmate()):
                check_value = 100
        else:
            number_move_black += 1
            if(temp_board.is_checkmate()):
                check_value = 100

    extra = 0
    for position in range(64):
        if(board.piece_at(position) == 'P'):
            board_value += position // 8
        if(board.piece_at(position) == 'p'):
            board_value -= position // 8

    # Formula to calculate the value of board for white
    board_value += 200*(list_of_pieces.count('K') - list_of_pieces.count('k'))
    board_value += 9*(list_of_pieces.count('Q') - list_of_pieces.count('q'))
    board_value += 5*(list_of_pieces.count('R') - list_of_pieces.count('r'))
    board_value += 3*(list_of_pieces.count('B') - list_of_pieces.count('b') + list_of_pieces.count('N') - list_of_pieces.count('n'))
    board_value -= 0.1*(+number_move_white - number_move_black)

    
    if (AI == "black"):
        return board_value + check_value
    else:
        return -1* board_value - check_value

# Check the requirement that the pieces must be eaten
def check_must_eat(board):

    # All the move that current player pieces moving to
    move_list = []
    move_list_2 = []
    moves = board.pseudo_legal_moves
    for move in moves:
        #print(change_char_to_value(str(move)[2:3]))
        move_list_2.append(move)
        move_list.append((int(str(move)[3:4]) - 1)*8 + (ord(str(move)[2:3])- ord('a')) )
    
    # curr player colour
    curr_player  = board.turn
    counter = 0
    posible_move = []
    #Iteration for the move in the board
    for move in move_list:
        # Check if the board has any pieces
        if(board.piece_at(move) != None):
            #If curr_player is not that colour
            if(curr_player != board.piece_at(move).color):
                posible_move.append(move_list_2[counter])
        counter += 1

    return posible_move

def legal_move(game_board):
    legal_move_list = []
    for move in game_board.legal_moves:
         legal_move_list.append(str(move))
    return legal_move_list

def player_ai_switch(game_board, player_ai, move):

    game = True

    if(player_ai == "player"):
        #########################         Player       ######################################
        valid_command = True;
        # For player easier to track all their valid moves
        move_list = []
        for move in game_board.legal_moves:
            move_list.append(str(move))
        print("Legal move: ", move_list)

        # To check if the move is must_eat move
        if(check_must_eat(game_board) == []):
            player_turn = input("Enter command: ")
        else:
            only_move = []
            for list in check_must_eat(game_board):
                only_move.append(str(list))

            while(valid_command):
                player_turn = input("Enter command: ")
                if(player_turn in only_move):
                    valid_command = False;
                else:
                    print("Invalid command. Kill the piece",only_move)

        game_board.push_uci(player_turn)
        print(game_board)
        print("Player move: ", player_turn)
        print()

        return player_turn;

    #########################             AI            ######################################
    if(player_ai == "AI"):
        if(game_board.turn == True):
             value , bestmove = alphaBetaMax(game_board, -100000 ,100000,2,"white",move)
             if(bestmove == None):
                return bestmove
             if str(bestmove) not in legal_move(game_board):
                return None
             else:
                game_board.push_uci(str(bestmove))
        else:
             value , bestmove = alphaBetaMax(game_board, -100000 ,100000,2,"black",move)
             if(bestmove == None):
                return bestmove
             if str(bestmove) not in legal_move(game_board):
                return None
             else:
                game_board.push_uci(str(bestmove))

        print(game_board)
        print("AI move: ", bestmove)
        print()

        return bestmove;



def main():  
    game_board  = chess.Board()
    print("========================")
    print("= CO 456 Final Project =")
    print("= Welcome to Chess 1.0 =")
    print("= Built by      MCZ    =")
    print("========================")
    game = True;

    #player_side = input("Player can choose (white/black):")

    # Prompt user to choose their side
    player_side = input("Choose our AI on (white/black) side: ")
    while(True):
        if(player_side == "white"):
            white_player = "AI"
            black_player = "player"
            break;
        elif(player_side == "black"):
            white_player = "player"
            black_player = "AI"
            break;
        else: 
            print("Invalid command")
            player_side = input("Please try again:")

    counter = 0;

    repeat_move_white = None;
    repeat_move_black = None;

    # While game is still on
    while(game):
        #########   Player white
        print("-White Player move")
        repeat_move_white = player_ai_switch(game_board,white_player,repeat_move_white)

        if(repeat_move_white == None):
            print("white_player lose")
            game = False
            break

        ## condition for fifty_move
        if(game_board.can_claim_fifty_moves()):
            print("Draw game")
            break

        #########   Player black
        print("-Black Player move")
        repeat_move_black = player_ai_switch(game_board,black_player,repeat_move_black)
        if(repeat_move_black == None):
            print("black_player lose")
            game = False
            break

        if(game_board.can_claim_fifty_moves()):
            print("Draw game")
            break



if __name__ == "__main__":  
    sys.exit(int(main() or 0)) 
