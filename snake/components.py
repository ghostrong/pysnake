#coding=utf8


import curses
import random
import config


class Apple(object):

    def __init__(self, y, x):
        self.position = (y, x)


class Snake(object):

    def __init__(self):
        center_y = config.BOARD_HEIGHT / 2
        center_x = config.BOARD_WIDTH / 2
        self.bodies = []
        start = center_x - config.INIT_SNAKE_SIZE / 2
        for i in xrange(config.INIT_SNAKE_SIZE):
            seg = (center_y, start+i)
            self.bodies.append(seg)
        self.direction = config.DIRECTION_MAPPER['LEFT']
        self.speed = config.INIT_SNAKE_SPEED
        self.dead_seg = None
        self.growth = False

    def move(self):
        new_head = (self.bodies[0][0] + self.direction[0] * self.speed,
                    self.bodies[0][1] + self.direction[1] * self.speed)
        self.bodies.insert(0, new_head)
        if self.growth:
            self.growth = False
        else:
            self.dead_seg = self.bodies.pop()


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
            config.PADDING_LEFT,
            config.PADDING_LEFT + config.BOARD_WIDTH,
            config.PADDING_TOP,
            config.PADDING_TOP + config.BOARD_HEIGHT,
        )
        self.init_color()
        self.score = 0

    def reset(self):
        self.score = 0
        self.draw_ground()
        self.draw_boundry()
        self.draw_score()
        self.born_snake()
        self.draw_snake()
        self.apples = []
        for i in xrange(config.INIT_APPLE_NUM):
            a = self.produce_apple()
            self.draw_apple(a)

    def beat(self, msg):
        self.screen.addstr(0, 0, msg, self.color_mapper['TEXT'])
        self.screen.refresh()

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
        _y = config.PADDING_TOP + y
        _x = config.PADDING_LEFT + x * 2
        self.screen.addstr(_y, _x, char, color)
        if len(char) == 1:
            self.screen.addstr(_y, _x+1, char, color)

    def born_snake(self):
        self.snake = Snake()

    def draw_boundry(self):
        color = self.color_mapper['BORDER']
        for y in xrange(0, config.BOARD_HEIGHT):
            self.draw_cell(y, 0, ' ', color)
            self.draw_cell(y, config.BOARD_WIDTH, ' ', color)
        for x in xrange(0, config.BOARD_WIDTH + 1):
            self.draw_cell(0, x, ' ', color)
            self.draw_cell(config.BOARD_HEIGHT, x, ' ', color)

        help_infos = [
            '[R]reset',
            '[Q]quit',
            '[H]left',
            '[J]down',
            '[K]up',
            '[L]right',
            '[[]speed-',
            '[]]speed+',
            '[ ]pause',
        ]
        helpstr = ' '.join(help_infos)
        self.draw_cell(-2, 1, helpstr, self.color_mapper['TEXT'])
        self.screen.refresh()

    def draw_ground(self):
        color = self.color_mapper['GROUND']
        for x in xrange(1, config.BOARD_WIDTH):
            for y in xrange(1, config.BOARD_HEIGHT):
                self.draw_cell(y, x, ' ', color)
        self.screen.refresh()

    def draw_snake(self):
        color = self.color_mapper['SNAKE']
        for y, x in self.snake.bodies:
            self.draw_cell(y, x, ' ', color)
        if self.snake.dead_seg:
            if self.snake.growth:
                self.snake.growth = False
            else:
                y, x = self.snake.dead_seg
                self.draw_cell(y, x, ' ', self.color_mapper['GROUND'])
            self.snake.dead_seg = None
        self.screen.refresh()

    def produce_apple(self):
        y = random.randrange(1, config.BOARD_HEIGHT)
        x = random.randrange(1, config.BOARD_WIDTH)

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

    def draw_score(self):
        score_str = 'SCORE: %s' % self.score
        self.draw_cell(-1, 1, score_str, self.color_mapper['TEXT'])

    def check_eating(self):
        y, x = self.snake.bodies[0]
        idx = -1
        for i, apple in enumerate(self.apples):
            if apple.position[0] == y and apple.position[1] == x:
                idx = i
                break
        if idx >= 0:
            self.apples[idx] = self.apples[-1]
            self.apples.pop()
            a = self.produce_apple()
            self.draw_apple(a)
            self.snake.growth = True
            self.score += 2
            self.draw_score()
            return True
        return False

    def check_out_bounds(self):
        y, x = self.snake.bodies[0]
        if y <= 0 or y >= config.BOARD_HEIGHT or x <= 0 or x >= config.BOARD_WIDTH:
            return True
        return False

    def gameover(self):
        self.draw_ground()
        self.draw_boundry()
        self.snake = None
        self.apples = []
        center_y = config.BOARD_HEIGHT / 2
        center_x = config.BOARD_WIDTH / 2
        self.draw_cell(center_y, center_x-4, 'Game Over', self.color_mapper['TEXT'])
        self.screen.refresh()


if __name__ == '__main__':
    config.init()
    b = Board()
    try:
        b.reset()
        while True:
            pass
    except Exception as e:
        pass
    finally:
        b.exit()
