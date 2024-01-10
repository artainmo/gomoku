from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Board():
    def __init__(self):
        self.rows = 19
        self.cols = 19
        self.positions = []
        for i in range(19):
            row = []
            for l in range(19):
                row.append(None)
            self.positions.append(row)

    def get_position_value(self, row, col):
        return self.positions[row][col]

    def set_position(self, row, col, pawn_value):
        self.positions[row][col] = pawn_value #None, white or black

board = Board()
turn = None

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("game.html", board_size=45, board=board, turn=turn)

@app.route('/start')
def start():
    global turn
    turn = 'white'
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    global turn
    global board
    board = Board()
    turn = None
    return redirect(url_for('index'))

@app.route('/place_pawn', methods=["POST"])
def place_pawn():
    global turn
    starting_time = 0
    row = int(request.args.get('row'))
    col = int(request.args.get('col'))
    if board.get_position_value(row, col) == None:
        board.set_position(row, col, turn)
        turn = 'black' if turn == 'white' else 'white'
    else:
        return ('', 204) #Don't return anything if no pawn is placed
    return redirect(url_for('index'))
