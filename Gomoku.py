from flask import Flask, render_template, request, redirect, url_for
from src.verify_pawns import verify_winning_alignment, verify_capture, \
            verify_captured_position, num_free_three_alignments

app = Flask(__name__)

class Board():
    def __init__(self):
        self.rows = 19
        self.cols = 19
        self.positions = []
        for i in range(self.rows):
            row = []
            for l in range(self.cols):
                row.append(None)
            self.positions.append(row)
        self.captures = { "white": 0, "black": 0 }

    def get_position_value(self, row, col):
        if row < 0 or row > 18 or col < 0 or col > 18:
            return None
        return self.positions[row][col]

    def set_position(self, row, col, pawn_value):
        if row < 0 or row > 18 or col < 0 or col > 18:
            return
        self.positions[row][col] = pawn_value #None, white or black

board = Board()
turn = None
win = None
play_against_AI = False

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("game.html", board_size=45, board=board,
                turn=turn, win=win, play_against_AI=play_against_AI)

@app.route('/start', methods=["POST"])
def start():
    global turn
    global play_against_AI
    turn = 'white'
    if request.args.get('adversary') == 'AI':
        play_against_AI = True
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    global turn
    global board
    global win
    global play_against_AI
    board = Board()
    turn = None
    win = None
    board.captures["white"] = 0
    board.captures["black"] = 0
    play_against_AI = False
    return redirect(url_for('index'))

@app.route('/place_pawn', methods=["POST"])
def place_pawn():
    global turn
    global win
    starting_time = 0
    row = int(request.args.get('row'))
    col = int(request.args.get('col'))
    if turn and board.get_position_value(row, col) == None and \
                not verify_captured_position(board, turn, row, col) and \
                num_free_three_alignments(board, turn, row, col) < 2:
        board.set_position(row, col, turn)
        if verify_capture(board, turn):
            board.captures[turn] += 1
        turn = 'black' if turn == 'white' else 'white'
    else:
        return ('', 204) #Don't return anything if no pawn is placed
    if turn and (board.captures['black' if turn == 'white' else 'white'] >= 5 \
                or verify_winning_alignment(board, turn)): #verify previous color to give chance to losing color of capturing a pair and breaking alignment of winning color
        win = turn
        turn = None
    return redirect(url_for('index'))

from random import randint

@app.route('/AI_play', methods=["POST"])
def AI_play():
    return redirect(url_for('place_pawn', row=randint(0,19), col=randint(0,19)), code=307) #code set to 307 allows redirect to POST route