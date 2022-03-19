import datetime
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import pyqtgraph as pg
import numpy as np
from PyQt5.QtGui import QPicture, QPainter
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from matplotlib.dates import date2num

from qtpy import QtGui, QtCore


class CandleStickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        w = 0.4
        self.bPen = pg.mkPen(color=(0, 240, 240, 255), width=w * 2)
        self.bBrush = pg.mkBrush((0, 240, 240, 255))
        self.rPen = pg.mkPen(color=(255, 60, 60, 255), width=w * 2)
        self.rBrush = pg.mkBrush((255, 60, 60, 255))

        self.data = data
        self.generatePicture(data)

    def generatePicture(self, data, redraw=False):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)

        w = 0.4

        for index, row in data.iterrows():
            # 下跌蓝色（实心），上涨红色（空心）
            pen, brush, pmin, pmax = (self.bPen, self.bBrush, row["close"], row["open"]) if row["open"] > row["close"] else (
                self.rPen, self.rBrush, row["open"], row["close"])
            p.setPen(pen)
            p.setBrush(brush)

            if row["low"] == row["high"]:
                p.drawRect(QtCore.QRectF(index - w, row["open"], w * 2, row["close"] - row["open"]))
            else:
                p.drawLine(QtCore.QPointF(index, row["low"]), QtCore.QPointF(index, row["high"]))
                p.drawRect(QtCore.QRectF(index - w, row["open"], w * 2, row["close"] - row["open"]))
        p.end()
        return p

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())