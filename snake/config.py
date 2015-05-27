#coding=utf8


import curses
import fcntl
import struct
import sys
import termios


LATENCY = 0.2

KEY_MAPPER = {
    'LEFT': [ord('h'), ord('H')],
    'RIGHT': [ord('l'), ord('L')],
    'UP': [ord('k'), ord('K')],
    'DOWN': [ord('j'), ord('J')],
    'QUIT': [ord('q'), ord('Q')],
    'RESET': [ord('r'), ord('R')],
    'SPEED+': [ord(']')],
    'SPEED-': [ord('[')],
    'PAUSE': [ord(' ')],
}

INIT_SNAKE_SIZE = 5

INIT_SNAKE_SPEED = 1

INIT_APPLE_NUM = 3

PADDING_LEFT = 10
PADDING_TOP = 5

TERM_HEIGHT, TERM_WIDTH = (40, 80)

COLOR_MAPPER = {
    'GROUND': (curses.COLOR_WHITE, curses.COLOR_WHITE),
    'APPLE': (curses.COLOR_RED, curses.COLOR_RED),
    'SNAKE': (curses.COLOR_GREEN, curses.COLOR_GREEN),
    'BORDER': (curses.COLOR_WHITE, curses.COLOR_CYAN),
    'TEXT': (curses.COLOR_GREEN, curses.COLOR_WHITE),
}

DIRECTION_MAPPER = {
    'LEFT': (0, -1),
    'RIGHT': (0, +1),
    'UP': (-1, 0),
    'DOWN': (+1, 0),
}


def get_terminal_size():
    s = struct.pack('HHHH', 0, 0, 0, 0)
    t = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s)
    ut = struct.unpack('HHHH', t)
    height, width = ut[0], ut[1]
    return (height, width)


def init():
    global TERM_HEIGHT
    global TERM_WIDTH
    TERM_HEIGHT, TERM_WIDTH = get_terminal_size()
    global BOARD_HEIGHT
    global BOARD_WIDTH
    BOARD_HEIGHT = TERM_HEIGHT - PADDING_TOP * 2
    BOARD_WIDTH = (TERM_WIDTH - PADDING_LEFT * 2) / 2
