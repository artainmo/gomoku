
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

def alignments_with_max_one_hole(board, color, row1, col1, row2, col2):
    alignment = 1
    empty_position = 1
    row_angle = row2 - row1
    col_angle = col2 - col1
    row0 = row1 - row_angle
    col0 = col1 - col_angle
    while board.get_position_value(row0, col0) == color or empty_position:
        if board.get_position_value(row0, col0) != color:
            if board.get_position_value(row0-row_angle, col0-col_angle) == color:
                empty_position -= 1
                alignment -= 1
            else:
                break
        alignment += 1
        row0 -= row_angle
        col0 -= col_angle
    while board.get_position_value(row2, col2) == color or empty_position:
        if board.get_position_value(row2, col2) != color:
            if board.get_position_value(row2+row_angle, col2+col_angle) == color:
                empty_position -= 1
                alignment -= 1
            else:
                break
        alignment += 1
        row2 += row_angle
        col2 += col_angle
    if board.get_position_value(row0, col0) == None:
        open_start = True
    else:
        open_start = False
    if board.get_position_value(row2, col2) == None:
        open_end = True
    else:
        open_end = False
    return alignment, open_start, open_end

def free_three_alignment(board, color, row1, col1, row2, col2):
    alignment, open_start, open_end = alignments_with_max_one_hole(board, color, row1, col1, row2, col2)
    if alignment == 3 and open_start and open_end:
        return True
    return False

def num_free_three_alignments(board, color, row, col):
    num = 0
    next_neighbour_positions = [
        { "row": row, "col": col+1 },
        { "row": row+1, "col": col+1 },
        { "row": row+1, "col": col },
        { "row": row+1, "col": col-1 }
    ]
    for neighbour in next_neighbour_positions:
        if free_three_alignment(board, color, row, col,
                    neighbour["row"], neighbour["col"]):
            num += 1
    return num
