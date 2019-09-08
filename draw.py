from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import PyQt5.QtGui as QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import *
from collections import deque
import logging
import time
from collections import deque

log = logging.getLogger('draw func')
FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)


class Draw:
    def __init__(self, board):
        self.board = board
        self._offset = 15
        self.width = 0
        self.height = 0
        self.last = time.time()
        self.field_width = -1
        self.field_length = -1
        self.lines = []
        self.queue = deque([])
        self.block_thread = False

    def draw_lines(self, data):
        tmp = time.time() - self.last
        if tmp > 0.05:
            self.last = time.time()
            self.board.scene().clear()

        for line in self.lines:
            self.board.scene().addItem(QGraphicsLineItem(*line))

        geo = data[0]
        robots = data[1]

        scale_w = 0
        scale_h = 0

        if geo.field.field_length != 0 and geo.field.field_width != 0:
            self.field_width = geo.field.field_width
            self.field_length = geo.field.field_length
        try:
            scale_w = self.board.width / self.field_length
            scale_h = self.board.height / self.field_width
        except ZeroDivisionError:
            print(0)

        self.width = self.field_width
        self.height = self.field_length

        # for item in geo.field.field_lines:
        #     p1 = item.p1
        #     p2 = item.p2
        #     x1, y1 = p1.x * scale_w + int(self.board.width / 2), p1.y * scale_h + int(self.board.height / 2)
        #     x2, y2 = p2.x * scale_w + int(self.board.width / 2), p2.y * scale_h + int(self.board.height / 2)
        #     x1, y1, x2, y2 = x1 + self._offset, y1 + self._offset, x2 + self._offset, y2 + self._offset
        #     self.lines.append([x1, y1, x2, y2])
        #     self.board.scene().addItem(QGraphicsLineItem(x1, y1, x2, y2))
        #     # self.board.viewport().update()
        # # self.board.viewport().update()

        for item in robots.robots_yellow:
            _x, _y = item.x * scale_w + int(self.board.width / 2), item.y * scale_h + int(self.board.height / 2)
            self._draw_robot(int(_x), int(_y))

        for item in robots.robots_blue:
            _x, _y = item.x * scale_w + int(self.board.width / 2), item.y * scale_h + int(self.board.height / 2)
            self._draw_robot(_x, _y)

    def add2queue(self, data):
        if len(self.queue) != 0:
            self.draw_lines(self.queue.popleft())
        self.queue.append(data)

    def _draw_robot(self, x, y):
        self.board.scene().addItem(QGraphicsEllipseItem(x + 10, y + 10, 20, 20))

    def draw_balls(self, data):
        pass
