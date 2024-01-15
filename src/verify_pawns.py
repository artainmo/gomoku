
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

def alignments_with_max_one_hole(board, color, row1, col1, row2, col2, remember=None):
    alignment = 1
    empty_position = 1
    row_angle = row2 - row1
    col_angle = col2 - col1
    row0 = row1 - row_angle
    col0 = col1 - col_angle
    while board.get_position_value(row0, col0) == color or \
                (board.get_position_value(row0, col0) == None and empty_position):
        if board.get_position_value(row0, col0) == None:
            if board.get_position_value(row0-row_angle, col0-col_angle) == color:
                empty_position -= 1
                alignment -= 1
            else:
                break
        alignment += 1
        row0 -= row_angle
        col0 -= col_angle
    while board.get_position_value(row2, col2) == color or \
                (board.get_position_value(row2, col2) == None and empty_position):
        if board.get_position_value(row2, col2) == None:
            if board.get_position_value(row2+row_angle, col2+col_angle) == color:
                empty_position -= 1
                alignment -= 1
            else:
                break
        if remember != None: #memorize the reviewed positions that come next to avoid reviewing them again
            remember.append({"row": row2, "col": col2})
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
    if empty_position == 0:
        hole = True
    else:
        hole = False
    if remember == None:
        return alignment, open_start, open_end, hole
    else:
        return alignment, open_start, open_end, hole, row0, col0, row2, col2

def free_three_alignment(board, color, row1, col1, row2, col2):
    alignment, open_start, open_end, hole = \
                alignments_with_max_one_hole(board, color, row1, col1, row2, col2)
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

def alignment_open_for_five_and_future_end(board, color, row_start, col_start, row_end,
            col_end, row_angle, col_angle, open_start, open_end, alignment, hole):
    decay_factor1 = 0
    decay_factor2 = 0
    if open_start:
        while board.get_position_value(row_start, col_start) == color or \
                board.get_position_value(row_start, col_start) == None: #and \ # In theory those conditions should be present too. But they slow down the algorithm too much and are not of high importance thus I removed them.
                #not verify_captured_position(board, color, row_start, col_start) and \
                #num_free_three_alignments(board, color, row_start, row_start) < 2):
            row_start -= row_angle
            col_start -= row_angle
            decay_factor1 += 1
            if alignment + hole + decay_factor1 >= 5 and decay_factor1 > 3:
                break
    if open_end:
        while board.get_position_value(row_end, col_end) == color or \
                board.get_position_value(row_end, col_end) == None: #and \
                #not verify_captured_position(board, color, row_end, col_end) and \
                #num_free_three_alignments(board, color, row_end, col_end) < 2):
            row_start += row_angle
            col_start += row_angle
            decay_factor2 += 1
            if alignment + hole + decay_factor1 + decay_factor2 >= 5 and decay_factor2 > 3:
                break
    if alignment + hole + decay_factor1 + decay_factor2 > 4:
        openForFive = True
    else:
        openForFive = False
    return openForFive, min(decay_factor1, decay_factor2)

def alignment_score(board, color, row1, col1, row2, col2, remember):
    row_angle = row2 - row1
    col_angle = col2 - col1
    alignment, open_start, open_end, hole, row_start, col_start, row_end, col_end = \
            alignments_with_max_one_hole(board, color, row1, col1, row2, col2, remember)
    if hole:
        hole = 1
    else:
        hole = 0
    if alignment == 2 and hole and open_end:
        if board.get_position_value(row_end+row_angle, col_end+col_angle) == color:
            remember.append({"row": row_end+row_angle, "col": col_end+col_angle})
            alignment += 1
            hole += 1
    openForFive, decay_factor = alignment_open_for_five_and_future_end(board, color,
            row_start, col_start, row_end, col_end, row_angle, col_angle,
            open_start, open_end, alignment, hole)
    return alignment, hole, open_start, open_end, openForFive, decay_factor
