
def pawn_alignment(board, color, row1, col1, row2, col2):
    alignment = 0
    row_angle = row1 - row2
    col_angle = col1 - col2
    while board.get_position_value(row2, col2) == color:
        alignment += 1
        row2 += row_angle
        col2 += col_angle
    return alignment

def neighbouring_pawns(board, color, row, col):
    next_neighbour_positions = [
        { "row": row, "col": col+1 },
        { "row": row+1, "col": col+1},
        { "row": row+1, "col": col},
        { "row": row+1, "col": col-1}
    ]
    for neighbour in next_neighbour_positions:
        print(neighbour)
        if board.get_position_value(neighbour["row"], neighbour["col"]) == color:
            yield neighbour

def verify_winning_alignment(board, color):
    for row in range(board.rows):
        for col in range(board.cols):
            if board.get_position_value(row, col) == color:
                for neighbour in neighbouring_pawns(board, color, row, col):
                    if pawn_alignment(board, color, row, col,
                                neighbour["row"], neighbour["col"]) > 4:
                        return True
    return False
