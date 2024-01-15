import copy
from src.verify_pawns import verify_winning_alignment, verify_capture, \
            verify_captured_position, num_free_three_alignments, \
            alignment_score
from Gomoku import app

visualize = app.config['DEBUG']
potential_moves = []

def find_score_alignment(board, color, row, col, remember):
    for rem in remember:
        if rem["row"] == row and rem["col"] == col:
            return 0
    scores = []
    next_neighbour_positions = [
        { "row": row, "col": col+1 },
        { "row": row+1, "col": col+1},
        { "row": row+1, "col": col},
        { "row": row+1, "col": col-1}
    ]
    for neighbour in next_neighbour_positions:
        alignment, hole, open_start, open_end, openForFive, decay_factor = \
                    alignment_score(board, color, row,
                    col, neighbour["row"], neighbour["col"], remember)
        if not openForFive:
            continue
        ## "UCT-ADP Progressive Bias Algorithm for Solving Gomoku" (https://arxiv.org/pdf/1912.05407.pdf)
        ## page 3, hard-coding heuristic patterns
        # if alignment >= 5 and hole == 0:
        #     score += 10 ** 5
        # elif alignment == 4 and hole == 0 and open_start and open_end:
        #     score += 10 ** 4
        # elif alignment == 4 and hole == 0 and (open_start or open_end):
        #     score += 10 ** (4-1)
        # elif alignment == 4 and hole == 1 and (open_start or open_end):
        #     score += (10 ** (4-1)) * 0.9
        # elif alignment == 3 and hole == 0 and decay_factor >= 2:
        #     score += 10 ** 3
        # elif alignment == 3 and hole == 0 and open_start and open_end:
        #     score += (10 ** 3) * 0.9
        # elif alignment == 3 and hole == 0 and (open_start or open_end):
        #     score += 10 * (3-1)
        # elif alignment == 3 and hole == 1 and open_start and open_end:
        #     score += (10 ** 3) * 0.9
        # elif alignment == 3 and hole == 1 and (open_start or open_end):
        #     score += (10 ** (3-1)) * 0.9
        # elif alignment == 3 and hole == 2 and open_start and open_end:
        #     score += 10 * (3-1)
        # elif alignment == 2 and hole == 0 and decay_factor >= 3:
        #     score += 10 * 2
        ## Using formula to handle all 32 cases instead
        base = 10
        power = alignment
        modulate = 1
        if (open_start and not open_end) or (not open_start and open_end):
            power -= 1
        elif decay_factor < 5 - alignment:
            modulate -= 0.1
        if hole == 1:
            modulate -= 0.1
        if hole == 2:
            power -= 1
        #The two following ifs try to force AI into stopping the player from winning when he is about to
        if color == "white" and alignment == 4 and (open_start or open_end):
            power += 1
        elif color == "white" and alignment == 3 and open_start and open_end:
            power += 1
        score = (base ** power) * modulate
        scores.append(score)
        if visualize and color == "black":
            global potential_moves
            potential_moves.append({
                "color": color,
                "position": (row, col),
                "direcion": (neighbour["row"]-row, neighbour["col"]-col),
                "alignment": alignment,
                "holes": hole,
                "open start": open_start,
                "open end": open_end,
                "open for five": openForFive,
                "closest closing alignment": decay_factor,
                "score": score
            })
    return sum(scores)

def heuristic(board, color):
    score = 0
    #Addition all captures of our player and substract all captures of adversary
    score += 9 ** board.captures[color]
    score -= 9 ** board.captures['white' if color == 'black' else 'black']
    #Addition all alignments (with max one hole) of our player and substract those of adversary
    remember = []
    for row in range(board.rows):
        for col in range(board.cols):
            if board.get_position_value(row, col) == color:
                score += find_score_alignment(board, color, row, col, remember)
            elif board.get_position_value(row, col) == ('white' if color == 'black' else 'black'):
                score -= find_score_alignment(board,
                        'white' if color == 'black' else 'black', row, col, remember)
    return score

def generate_positions(board, color):
    for row in range(board.rows):
        for col in range(board.cols):
            next_neighbour_positions = [
                { "row": row, "col": col+1 },
                { "row": row+1, "col": col+1},
                { "row": row+1, "col": col},
                { "row": row+1, "col": col-1},
                { "row": row, "col": col-1},
                { "row": row-1, "col": col-1},
                { "row": row-1, "col": col}
            ]
            if any(board.get_position_value(neighbour["row"], neighbour["col"])
                        in ["white", "black"] for neighbour in next_neighbour_positions): #Only review positions who are next to actual stones
                if board.get_position_value(row, col) == None and \
                            not verify_captured_position(board, color, row, col) and \
                            num_free_three_alignments(board, color, row, col) < 2:
                    new_board = copy.deepcopy(board)
                    new_board.set_position(row, col, color)
                    if verify_capture(new_board, color):
                        new_board.captures[color] += 1
                    yield [new_board, (row, col)]

next_move = (None, None)

#The minimax algorithm will try out all possible positions for a certain amount of turns to find the best position for each turn and have the best game at the end of those turns.
#It will find the best positions for itself while assuming the other player to also play the best moves possible.
#Alpha and beta are used for the Alpha-beta pruning technique which fastens the minimax algorithm by stopping search of moves once we know we cannot find a better move.
#Visualize the algorithm via this video (https://www.youtube.com/watch?v=l-hh51ncgDI)
def minimax(board, depth, maximizingPlayer=True, alpha=float('-inf'), beta=float('inf')):
    global next_move
    if depth == 0 or board.captures['white' if maximizingPlayer else 'black'] >= 5 \
                or verify_winning_alignment(board, 'black' if maximizingPlayer else 'white'): #After going through all turns or after the game ends it will stop searching and return the evaluation of current game.
        return heuristic(board, 'black') #The heuristic gives a score on how well positioned a player is in its game.
    if maximizingPlayer: #Here we will search the best move for the player we want to win.
        maxEval = float('-inf')
        for [new_position_board, move] in generate_positions(board, 'black'): #We go over all next playable positions.
            eval = minimax(new_position_board, depth-1, False, alpha, beta) #We recursively call minimax to search for moves of next turns.
            if eval > maxEval:
                # print("--------------")
                # print("Depth: ", depth)
                # print("maxEval: ", eval)
                # print("alpha: ", eval)
                # print("beta: ", beta)
                # print("--------------")
                maxEval = eval #We memorize the best move for us which has highest score from heuristic function.
                next_move = move
                alpha = eval #Alpha refers to best score/move(s) of our player. While beta refers to worst score or best move of adversary.
                #The lowest alpha value or worst score/move of our player will become the best move (worst score) of adversary which beta refers to.
                #For our player we will remember the highest value stored in alpha. The adversary will have to pick the lowest alpha from different moves.
                #If we already have an alpha greater than beta, we know if we keep searching we won't chose an alpha smaller than beta later on either way.
                #Thus the current beta will be remembered over the new beta that will consist of the highest alpha value we are currently searching.
                #Thus we know we can stop searching as the previous beta will be a better position for the adversary either way.
                if beta <= alpha:
                    break
        return maxEval
    else: #Here we will search the best move for the adversary as we assume he will play his best moves.
        minEval = float('inf')
        for [new_position_board, move] in generate_positions(board, 'white'):
            eval = minimax(new_position_board, depth-1, True, alpha, beta)
            if eval < minEval:
                # print("--------------")
                # print("Depth: ", depth)
                # print("minEval: ", eval)
                # print("alpha: ", alpha)
                # print("beta: ", eval)
                # print("--------------")
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

def print_move(move):
    print("color: ", move["color"])
    print("position: ", move["position"])
    print("direcion: ", move["direcion"])
    print("alignment: ", move["alignment"])
    print("holes: ", move["holes"])
    print("open start: ", move["open start"])
    print("open end: ", move["open end"])
    print("open for five: ", move["open for five"])
    print("closest closing alignment: ", move["closest closing alignment"])
    print("score: ", move["score"])
    print()

def run_minimax(board, depth):
    minimax(board, depth)
    if visualize:
        global potential_moves
        print("ALL REVIEWED MOVES")
        rem = []
        for move in potential_moves:
            if move["position"] not in rem:
                rem.append(move["position"])
                print(move["position"], end=", ")
        print("\n")
        print("BEST POTENTIAL MOVES")
        potential_moves.sort(key=lambda x:x["score"], reverse=True)
        print_move(potential_moves[0])
        print_move(potential_moves[1])
        print_move(potential_moves[2])
        potential_moves = []
    return next_move
