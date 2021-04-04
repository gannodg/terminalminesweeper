from board import Board
import curses
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr = curses.initscr()
    stdscr.clear()
    stdscr.keypad(True)
    stdscr.refresh()
    size = 16
    b = Board(size)

    display_hidden_board(stdscr, b)

    stdscr.move(8, 8*2)
    key_press = stdscr.getkey()
    while user_move(stdscr, key_press, b):
        stdscr.refresh()
        key_press = stdscr.getkey()
    key_press = stdscr.getkey()
    stdscr.clear()
    stdscr.refresh()
#    key_press = stdscr.getkey()

def display_board(stdscr, b):
    for i in range (0, b.size):
        for j in range (0, b.size):
            if b.G[i][j] and b.M[i][j] != 9 :
                stdscr.addstr(j, 2*i, "X", curses.A_REVERSE) 
            elif b.M[i][j] == 9 and b.G[i][j]:
                stdscr.addstr(j, 2*i, "@", curses.A_REVERSE)
            elif b.M[i][j] != 0 and b.M[i][j] != 9 and b.R[i][j]:
                stdscr.addstr(j, 2*i, str(b.M[i][j]))
            elif b.R[i][j] and b.M[i][j] == 0:
                stdscr.addstr(j, 2*i, " ")                
            elif b.M[i][j] == 9:
                stdscr.addstr(j, 2*i, "*", curses.A_REVERSE)
            else:
                stdscr.addstr(j, 2*i, ".")
    stdscr.addstr(b.size + 1, 0, "Bombs guessed: " + str(b.bombs_guessed))
    stdscr.addstr(b.size + 3, 0, "Arrow keys to move, Spacebar to guess, 'b' to toggle bombs, 'Q' to quit")
    stdscr.addstr(b.size + 2, 0, "Bombs left: " + str(b.bombs_left))

def display_hidden_board(stdscr, b):
    for i in range (0, b.size):
        for j in range (0, b.size):
            if b.G[i][j]:
                stdscr.addstr(j, 2*i, "b", curses.A_REVERSE)                
            elif b.R[i][j] and b.M[i][j] != 9 and b.M[i][j] != 0:
                stdscr.addstr(j, 2*i, str(b.M[i][j]))
            elif b.R[i][j] and b.M[i][j] == 0:
                stdscr.addstr(j, 2*i, " ")                
            else:
                stdscr.addstr(j, 2*i, ".")
    stdscr.addstr(b.size + 1, 0, "Bombs left: " + str(b.bombs_marked))
    stdscr.addstr(b.size + 3, 0, "Arrow keys to move, Spacebar to guess, 'b' to toggle bombs, 'Q' to quit")

def user_move(stdscr, key_press, b):
    pos = stdscr.getyx()
    if key_press == "KEY_LEFT":
        result = True
        if pos[1] > 0:
            stdscr.move(pos[0], pos[1] - 2)
    elif key_press == "KEY_RIGHT":
        result = True
        if pos[1] < ((b.size - 1) * 2):
            stdscr.move(pos[0], pos[1] + 2)
    elif key_press == "KEY_UP":
        result = True
        if pos[0] > 0:
            stdscr.move(pos[0] - 1, pos[1])
    elif key_press == "KEY_DOWN":
        result = True
        if pos[0] < (b.size - 1):
            stdscr.move(pos[0] + 1, pos[1])
    elif key_press == " ":
        result = True
        x = int(pos[1]/2)
        if b.visited(x,pos[0]):
            display_hidden_board(stdscr, b)
        else:
            display_board(stdscr, b)
            result = False
        stdscr.move(pos[0], pos[1])
    elif key_press == "b":
        result = True
        stdscr.addstr(pos[0], pos[1], "b", curses.A_REVERSE)
        x = int(pos[1]/2)
        if b.mark_bomb(x, pos[0]):
            stdscr.addstr(b.size + 1, 0, "Bombs left: " + str(b.bombs_marked))
            if b.bombs_left == 0:
                display_board(stdscr, b)
                result = 0
                stdscr.addstr(pos[0], b.size * 2 + 1, "Congratulations!")
            stdscr.move(pos[0], pos[1])
        else:
            stdscr.addstr(b.size + 1, 0, "Bombs left: " + str(b.bombs_marked))
            stdscr.addstr(pos[0], pos[1], ".")
            stdscr.move(pos[0], pos[1])
    else:
        result = False
    return result

wrapper(main)