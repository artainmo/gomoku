import copy
from src.verify_pawns import verify_winning_alignment, verify_capture, \
            verify_captured_position, num_free_three_alignments

def heuristic(board, color):
    score = 0
    score += board.captures[color]
    score -= board.captures['white' if color == 'black' else 'black']
    #TODO: score based on alignments that are open for continuity
    return score

def generate_positions(board, color):
    for row in range(self.rows):
        for col in range(self.cols):
            if board.get_position_value(row, col) == None and \
                        not verify_captured_position(board, color, row, col) and \
                        num_free_three_alignments(board, color, row, col) < 2:
                new_board = copy.deepcopy(board)
                new_board.set_position(row, col, color)
                if verify_capture(new_board, color):
                    new_board.captures[color] += 1
                yield new_board, (row, col)

#The minimax algorithm will try out all possible positions for a certain amount of turns to find the best position for each turn and have the best game at the end of those turns.
#It will find the best positions for itself while assuming the other player to also play the best moves possible.
#Alpha and beta are used for the Alpha-beta pruning technique which fastens the minimax algorithm by stopping search of moves once we know we cannot find a better move.
#Visualize the algorithm via this video (https://www.youtube.com/watch?v=l-hh51ncgDI)
def minimax(board, depth, maximizingPlayer, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or board.captures['white' if maximizingPlayer else 'black'] >= 5 \
                or verify_winning_alignment(board, 'black' if maximizingPlayer else 'white'): #After going through all turns or after the game ends it will stop searching and return the evaluation of current game.
        return heuristic(board, 'black') #The heuristic gives a score on how well positioned a player is in its game.
    if maximizingPlayer: #Here we will search the best move for the player we want to win.
        maxEval = float('-inf')
        move = (None, None)
        for new_position_board, (row, col) in generate_positions(board, 'black'): #We go over all next playable positions.
            eval = minimax(new_position_board, depth-1, False, alpha, beta) #We recursively call minimax to search for moves of next turns.
            if eval > maxEval:
                maxEval = eval #We memorize the best move for us which has highest score from heuristic function.
                move = (row, col)
                alpha = eval #Alpha refers to best score/move(s) of our player. While beta refers to worst score or best move of adversary.
                #The lowest alpha value or worst score/move of our player will become the best move (worst score) of adversary which beta refers to.
                #For our player we will remember the highest value stored in alpha. The adversary will have to pick the lowest alpha from different moves.
                #If we already have an alpha greater than beta, we know if we keep searching we won't chose an alpha smaller than beta later on either way.
                #Thus the current beta will be remembered over the new beta that will consist of the highest alpha value we are currently searching.
                #Thus we know we can stop searching as the previous beta will be a better position for the adversary either way.
                if beta <= alpha:
                    break
        return maxEval, move
    else: #Here we will search the best move for the adversary as we assume he will play his best moves.
        minEval = float('inf')
        for available_position in generate_positions(board, 'white'):
            eval = minimax(new_position_board, depth-1, True, alpha, beta)
            if eval < minEval:
                minEval = eval #We memorize the best move for the adversary which has lowest score from heuristic function.
                beta = eval
                #The highest beta value or worst move for adversary will become the best move for our player.
                #For adversary we will remember the lowest score stored in beta. Our player will have to pick the highest beta from different moves.
                #If we already have a beta smaller than alpha, if we keep searching we know we won't pick a beta greater than alpha later on either way.
                #Thus the current alpha will be remembered over the new alpha that will consist of the lowest beta value.
                #Thus we know we can stop searching as the previous alpha will be a better position for our player either way.
                if beta <= alpha:
                    break
        return minEval
