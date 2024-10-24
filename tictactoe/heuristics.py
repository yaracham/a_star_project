from state import *

def HEURISTIC(state):
    x3 = 0
    x2 = 0
    x1 = 0
    o3 = 0
    o2 = 0
    o1 = 0

    # check row wise
    for r in range(0, size):
        os = 0
        xs = 0
        for c in range(0, size):
            if state.table[r, c] == x_player:
                xs += 1
            elif state.table[r, c] == o_player:
                os += 1

        if xs == 0:
            if os == 1:
                o1 += 1
            elif os == 2:
                o2 += 1
            elif os == 3:
                o3 += 1

        if os == 0:
            if xs == 1:
                x1 += 1
            elif xs == 2:
                x2 += 1
            elif xs == 3:
                x3 += 1

    # check column wise
    for c in range(0, size):
        os = 0
        xs = 0
        for r in range(0, size):
            if state.table[r, c] == x_player:
                xs += 1
            elif state.table[r, c] == o_player:
                os += 1

        if xs == 0:
            if os == 1:
                o1 += 1
            elif os == 2:
                o2 += 1
            elif os == 3:
                o3 += 1

        if os == 0:
            if xs == 1:
                x1 += 1
            elif xs == 2:
                x2 += 1
            elif xs == 3:
                x3 += 1

    # check main diagonal
    os = 0
    xs = 0
    for i in range(0, size):
        if state.table[i, i] == x_player:
            xs += 1
        elif state.table[i, i] == o_player:
            os += 1

    if xs == 0:
        if os == 1:
            o1 += 1
        elif os == 2:
            o2 += 1
        elif os == 3:
            o3 += 1

    if os == 0:
        if xs == 1:
            x1 += 1
        elif xs == 2:
            x2 += 1
        elif xs == 3:
            x3 += 1

            # check main diagonal
    os = 0
    xs = 0
    for i in range(0, size):
        if state.table[size - i - 1, i] == x_player:
            xs += 1
        elif state.table[size - i - 1, i] == o_player:
            os += 1

    if xs == 0:
        if os == 1:
            o1 += 1
        elif os == 2:
            o2 += 1
        elif os == 3:
            o3 += 1

    if os == 0:
        if xs == 1:
            x1 += 1
        elif xs == 2:
            x2 += 1
        elif xs == 3:
            x3 += 1

    return (6 * x3 + 3 * x2 + x1) - (6 * o3 + 3 * o2 + o1)