from flask import Flask, render_template, request, redirect, url_for
from src.verify_pawns import verify_winning_alignment, verify_capture, \
            verify_captured_position

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
captures = { "white": 0, "black": 0 }

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("game.html", board_size=45, board=board,
                turn=turn, win=win, captures=captures)

@app.route('/start')
def start():
    global turn
    global win
    turn = 'white'
    win = None
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    global turn
    global board
    global win
    global captures
    board = Board()
    turn = None
    win = None
    captures["white"] = 0
    captures["black"] = 0
    return redirect(url_for('index'))

@app.route('/place_pawn', methods=["POST"])
def place_pawn():
    global turn
    global win
    starting_time = 0
    row = int(request.args.get('row'))
    col = int(request.args.get('col'))
    if turn and board.get_position_value(row, col) == None and \
                not verify_captured_position(board, turn, row, col):
        board.set_position(row, col, turn)
        if verify_capture(board, turn):
            captures[turn] += 1
        turn = 'black' if turn == 'white' else 'white'
    else:
        return ('', 204) #Don't return anything if no pawn is placed
    if verify_winning_alignment(board, turn): #verify previous color to give chance to losing color of capturing a pair and breaking alignment of winning color
        win = turn
        turn = None
    return redirect(url_for('index'))
