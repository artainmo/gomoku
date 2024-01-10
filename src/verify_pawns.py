
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

def pawn_capture(board, capture_color, row1, col1, row2, col2):
    row_angle = row1 - row2
    col_angle = col1 - col2
    print(row1+row_angle, col1+col_angle)
    print(row1, col1)
    print(row2, col2)
    print(row2-row_angle, col2-col_angle)
    if board.get_position_value(row2-row_angle, col2-col_angle) == capture_color \
                and board.get_position_value(row1+row_angle, col1+col_angle) \
                            == capture_color:
        return True
    return False

def verify_capture(board, capture_color):
    captured_color = 'black' if capture_color == 'white' else 'white'
    for row in range(board.rows):
        for col in range(board.cols):
            if board.get_position_value(row, col) == captured_color:
                for neighbour in neighbouring_pawns(board, captured_color, row, col):
                    if pawn_capture(board, capture_color, row, col,
                                neighbour["row"], neighbour["col"]):
                        board.set_position(row, col, None)
                        board.set_position(neighbour["row"], neighbour["col"], None)
                        return True
    return False

def all_neighbouring_pawns(board, color, row, col):
    next_neighbour_positions = [
        { "row": row, "col": col+1 },
        { "row": row+1, "col": col+1},
        { "row": row+1, "col": col},
        { "row": row+1, "col": col-1},
        { "row": row, "col": col-1},
        { "row": row-1, "col": col-1},
        { "row": row-1, "col": col}
    ]
    for neighbour in next_neighbour_positions:
        if board.get_position_value(neighbour["row"], neighbour["col"]) == color:
            yield neighbour

def verify_captured_position(board, captured_color, row, col):
    for neighbour in all_neighbouring_pawns(board, captured_color, row, col):
        if pawn_capture(board, 'black' if captured_color == 'white' else 'white', \
                    row, col, neighbour["row"], neighbour["col"]):
            return True
    return False
