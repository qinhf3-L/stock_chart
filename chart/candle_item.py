import pyqtgraph as pg

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
        data = data.fillna(0)
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)

        w = 0.4

        prema_3 = 0
        prema_5 = 0
        prema_10 = 0
        prema_20 = 0
        prema_30 = 0
        prema_60 = 0
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
            if prema_3 != 0:
                p.setPen(pg.mkPen('w', width=2))
                p.setBrush(pg.mkBrush('w'))
                p.drawLine(QtCore.QPointF(index - 1, prema_3), QtCore.QPointF(index, row["dema_3"]))
            prema_3 = row["dema_3"]
            if prema_5 != 0:
                p.setPen(pg.mkPen('c', width=2))
                p.setBrush(pg.mkBrush('c'))
                p.drawLine(QtCore.QPointF(index - 1, prema_5), QtCore.QPointF(index, row["dema_5"]))
            prema_5 = row["dema_5"]
            if prema_10 != 0:
                p.setPen(pg.mkPen('m', width=2))
                p.setBrush(pg.mkBrush('m'))
                p.drawLine(QtCore.QPointF(index - 1, prema_10), QtCore.QPointF(index, row["dema_10"]))
            prema_10 = row["dema_10"]
            if prema_20 != 0:
                p.setPen(pg.mkPen('k', width=2))
                p.setBrush(pg.mkBrush('k'))
                p.drawLine(QtCore.QPointF(index - 1, prema_20), QtCore.QPointF(index, row["dema_20"]))
            prema_20 = row["dema_20"]
            if prema_30 != 0:
                p.setPen(pg.mkPen('y', width=2))
                p.setBrush(pg.mkBrush('y'))
                p.drawLine(QtCore.QPointF(index - 1, prema_30), QtCore.QPointF(index, row["dema_30"]))
            prema_30 = row["dema_30"]
            if prema_60 != 0:
                p.setPen(pg.mkPen('b', width=2))
                p.setBrush(pg.mkBrush('b'))
                p.drawLine(QtCore.QPointF(index - 1, prema_60), QtCore.QPointF(index, row["dema_60"]))
            prema_60 = row["dema_60"]
        p.end()
        return p

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())