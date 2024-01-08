from flask import Flask, render_template, request

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
turn = 0

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        global turn
        turn += 1
        row = int(request.args.get('row'))
        col = int(request.args.get('col'))
        board.set_position(row, col, 'white' if turn % 2 else 'black')
    return render_template("game.html", board_size=40, board=board)
