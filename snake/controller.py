#coding=utf8


import time
import config
from components import Board


class Controller(object):

    def __init__(self):
        self.board = Board()
        self.screen = self.board.screen
        self.last_update = 0
        self.playing = False
        self.pausing = False
        self.latency = config.LATENCY
        self.delta = 0.05

    def exit(self):
        self.board.exit()

    def restart(self):
        self.board.reset()
        self.playing = True
        self.pausing = False
        self.latency = config.LATENCY

    def loop(self):
        self.restart()
        while True:
            bts = '%s   LATENCY:%s' % (time.ctime(), self.latency)
            self.board.beat(bts)
            key = self.screen.getch()
            if key in config.KEY_MAPPER['QUIT']:
                break
            if key in config.KEY_MAPPER['PAUSE'] and self.playing:
                self.pausing = not self.pausing
            if self.pausing:
                continue

            if key in config.KEY_MAPPER['RESET']:
                self.restart()
            elif not self.playing:
                continue
            elif key in config.KEY_MAPPER['LEFT']:
                if not self.board.snake.direction == config.DIRECTION_MAPPER['RIGHT']:
                    self.board.snake.direction = config.DIRECTION_MAPPER['LEFT']
            elif key in config.KEY_MAPPER['RIGHT']:
                if not self.board.snake.direction == config.DIRECTION_MAPPER['LEFT']:
                    self.board.snake.direction = config.DIRECTION_MAPPER['RIGHT']
            elif key in config.KEY_MAPPER['UP']:
                if not self.board.snake.direction == config.DIRECTION_MAPPER['DOWN']:
                    self.board.snake.direction = config.DIRECTION_MAPPER['UP']
            elif key in config.KEY_MAPPER['DOWN']:
                if not self.board.snake.direction == config.DIRECTION_MAPPER['UP']:
                    self.board.snake.direction = config.DIRECTION_MAPPER['DOWN']
            elif key in config.KEY_MAPPER['SPEED+']:
                if self.latency > self.delta:
                    self.latency -= self.delta
            elif key in config.KEY_MAPPER['SPEED-']:
                self.latency += self.delta

            time.sleep(self.delta)
            elapsed = time.time() - self.last_update
            if elapsed < self.latency:
                continue
                #time.sleep(self.latency - elapsed)

            self.board.snake.move()
            self.board.draw_snake()
            self.last_update = time.time()

            if self.board.check_out_bounds():
                self.playing = False
                self.board.gameover()
            else:
                self.board.check_eating()

