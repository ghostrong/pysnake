#!/usr/bin/env python
#coding=utf8


from snake import config
from snake.controller import Controller


def main():
    config.init()
    ctr = Controller()
    try:
        ctr.loop()
    except Exception as e:
        pass
    finally:
        ctr.exit()


if __name__ == '__main__':
    main()
