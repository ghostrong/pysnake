#coding=utf8


import curses
import random
import config


class Apple(object):

    def __init__(self, y, x):
        self.position = (y, x)


class Snake(object):

    def __init__(self):
        center_y = config.TERM_HEIGHT / 2
        center_x = config.TERM_WIDTH / 2
        self.bodies = []
        start = center_x - config.INIT_SNAKE_SIZE / 2
        for i in xrange(config.INIT_SNAKE_SIZE):
            seg = (center_y, start+i)
            self.bodies.append(seg)
        self.direction = config.DIRECTION_MAPPER['LEFT']

    def move(self):
        pass


class Board(object):

    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.screen.nodelay(1)
        curses.start_color()
        # LEFT, RIGHT, TOP, BOTTOM
        self.borders = (
            20,
            config.TERM_WIDTH - 20,
            5,
            config.TERM_HEIGHT - 5,
        )

        self.init_color()
        self.draw_ground()
        self.draw_boundry()
        self.born_snake()
        self.draw_snake()
        self.apples = []
        for i in xrange(config.INIT_APPLE_NUM):
            a = self.produce_apple()
            self.draw_apple(a)

    def exit(self):
        self.screen.clear()
        self.screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def init_color(self):
        self.color_mapper = {}
        for i, (key, color) in enumerate(config.COLOR_MAPPER.iteritems()):
            curses.init_pair(i+1, color[0], color[1])
            self.color_mapper[key] = curses.color_pair(i+1)

    def draw_cell(self, y, x, char, color):
        self.screen.addstr(y, x, char, color)
        self.screen.addstr(y, x+1, char, color)

    def born_snake(self):
        self.snake = Snake()

    def draw_boundry(self):
        left, right, top, bottom = self.borders
        color = self.color_mapper['BORDER']
        for y in xrange(top, bottom+1):
            self.draw_cell(y, left, ' ', color)
            self.draw_cell(y, right, ' ', color)
        for x in xrange(left, right+1):
            self.draw_cell(top, x, ' ', color)
            self.draw_cell(bottom, x, ' ', color)
        self.screen.refresh()

    def draw_ground(self):
        left, right, top, bottom = self.borders
        color = self.color_mapper['GROUND']
        for x in xrange(left+1, right):
            for y in xrange(top+1, bottom):
                self.draw_cell(y, x, ' ', color)
        self.screen.refresh()

    def draw_snake(self):
        color = self.color_mapper['SNAKE']
        for y, x in self.snake.bodies:
            self.draw_cell(y, x, ' ', color)
        self.screen.refresh()

    def produce_apple(self):
        left, right, top, bottom = self.borders
        y = random.randrange(top+1, bottom)
        x = random.randrange(left+1, right)

        for apple in self.apples:
            if apple.position[0] == y and apple.position[1] == x:
                return self.produce_apple()

        for seg in self.snake.bodies:
            if seg[0] == y and seg[1] == x:
                return self.produce_apple()

        apple = Apple(y, x)
        self.apples.append(apple)
        return apple

    def draw_apple(self, apple):
        color = self.color_mapper['APPLE']
        y, x = apple.position
        self.draw_cell(y, x, ' ', color)
        self.screen.refresh()


if __name__ == '__main__':
    config.init()
    try:
        b = Board()
        while True:
            pass
    except Exception as e:
        pass
    finally:
        b.exit()
