from board import Board
import curses
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
    stdscr.clear()
    stdscr.keypad(True)
    stdscr.refresh()

    size = choose_size(stdscr)
    play = True

    while play:
        stdscr.clear()
        stdscr.refresh()
        b = Board(size)

        display_hidden_board(stdscr, b)

        stdscr.move(int(size/2), size)
        key_press = stdscr.getkey()
        while user_move(stdscr, key_press, b):
            stdscr.refresh()
            key_press = stdscr.getkey()
        key_press = stdscr.getkey()
        if key_press == "c":
            size = choose_size(stdscr)
            play = True
        else:
            play = False
        stdscr.clear()
        stdscr.refresh()


def choose_size(stdscr):
    stdscr.clear()
    stdscr.refresh()
    stdscr.addstr(0, 0, "Welcome to Terminal Minesweeper")
    stdscr.addstr(1, 0, "1: 8 x 8 (default)")
    stdscr.addstr(2, 0, "2: 12 x 12")
    stdscr.addstr(3, 0, "3: 16 x 16")
    stdscr.addstr(4, 0, "4: 20 x 20")
    stdscr.addstr(5, 0, "Choose a size for the minefield:")

    key_press = stdscr.getkey()
    size = 8
    if key_press == "2":
        size = 12
    elif key_press == "3":
        size = 16
    elif key_press == "4":
        size = 20
    return size

def display_board(stdscr, b):
    stdscr.clear()
    stdscr.refresh()
    for i in range (0, b.size):
        for j in range (0, b.size):
            if b.G[i][j] and b.M[i][j] != 9 :
                stdscr.addstr(j, 2*i, "X", curses.A_REVERSE) 
            elif b.M[i][j] == 9 and b.G[i][j]:
                stdscr.addstr(j, 2*i, "@", curses.color_pair(2))
            elif b.M[i][j] != 0 and b.M[i][j] != 9 and b.R[i][j]:
                stdscr.addstr(j, 2*i, str(b.M[i][j]))
            elif b.R[i][j] and b.M[i][j] == 0:
                stdscr.addstr(j, 2*i, " ")                
            elif b.M[i][j] == 9:
                stdscr.addstr(j, 2*i, "*", curses.color_pair(3))
            else:
                stdscr.addstr(j, 2*i, ".")
    stdscr.addstr(b.size + 1, 0, "Bombs guessed: " + str(b.bombs_guessed))
    stdscr.addstr(b.size + 3, 0, "Press any key to quit, 'c' to play again.")
    stdscr.addstr(b.size + 2, 0, "Bombs left: " + str(b.bombs_left))


def display_hidden_board(stdscr, b):
    stdscr.clear()
    stdscr.refresh()
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
    stdscr.addstr(b.size + 3, 0, "Arrow keys to move, Spacebar to guess, 'b' to toggle bombs, 'q' to quit")

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
        x = int(pos[1]/2)
        if b.mark_bomb(x, pos[0]):
            stdscr.addstr(pos[0], pos[1], "b", curses.A_REVERSE)
            stdscr.addstr(b.size + 1, 0, "Bombs left: " + str(b.bombs_marked))
            if b.bombs_left == 0:
                display_board(stdscr, b)
                result = 0
                stdscr.addstr(pos[0], b.size * 2 + 1, "Congratulations!")
            stdscr.move(pos[0], pos[1])
        else:
            stdscr.addstr(b.size + 1, 0, "Bombs left: " + str(b.bombs_marked))
            if not b.R[x][pos[0]]:
                stdscr.addstr(pos[0], pos[1], ".")
            stdscr.move(pos[0], pos[1])
    elif key_press == "q":
        result = False
    else:
        result = True
    return result

####
#### This executes the program
####
wrapper(main)