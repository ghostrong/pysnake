#coding=utf8


import curses
import fcntl
import struct
import sys
import termios


LATENCY = 0.1

KEY_MAPPER = {
    'LEFT': [ord('h'), ord('H')],
    'UP': [ord('j'), ord('J')],
    'RIGHT': [ord('k'), ord('K')],
    'DOWN': [ord('l'), ord('L')],
}

INIT_SNAKE_SIZE = 5

INIT_APPLE_NUM = 3

TERM_HEIGHT, TERM_WIDTH = (40, 80)

COLOR_MAPPER = {
    'GROUND': (curses.COLOR_WHITE, curses.COLOR_WHITE),
    'APPLE': (curses.COLOR_RED, curses.COLOR_RED),
    'SNAKE': (curses.COLOR_GREEN, curses.COLOR_GREEN),
    'BORDER': (curses.COLOR_WHITE, curses.COLOR_YELLOW),
}

DIRECTION_MAPPER = {
    'LEFT': (-1, 0),
    'RIGHT': (1, 0),
    'UP': (0, -1),
    'DOWN': (0, 1),
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
