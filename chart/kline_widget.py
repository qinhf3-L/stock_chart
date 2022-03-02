import pandas as pd
import pyqtgraph as pg
from PyQt5.QtWidgets import QGridLayout, QLabel
from qtpy.QtGui import QFont
from qtpy.QtWidgets import QWidget, QVBoxLayout

from chart.candle_item import CandleStickItem
from chart.string_axis import StringAxis
from db.db import engine


class KLineWidget(QWidget):
    init_completed = False

    def __init__(self, ts_code=None):
        """Constructor"""
        super(KLineWidget, self).__init__()
        self.stock = None
        self.date_label = None
        self.weight_label = None
        self.chg_label = None
        self.low_label = None
        self.high_label = None
        self.close_label = None
        self.open_label = None
        self.lay_stock = None
        self.axisTime = StringAxis({}, orientation='bottom')
        self.pwKL = self.makePI('PlotKL')
        self.KLtitle = None
        self.vb = QVBoxLayout()
        self.load_data(ts_code)
        self.initUI()
        self.set_title()
        self.set_stock_info()
        self.plot_all()

    def initUI(self):
        """初始化界面"""
        self.pw = pg.PlotWidget()
        # 界面布局
        self.lay_KL = pg.GraphicsLayout(border=(100, 100, 100))
        self.lay_KL.setContentsMargins(10, 10, 10, 10)
        self.lay_KL.setSpacing(0)
        self.lay_KL.setBorder(color=(255, 0, 0, 255), width=0.8)
        self.lay_KL.setZValue(0)
        self.KLtitle = self.lay_KL.addLabel(u'')
        self.pw.setCentralItem(self.lay_KL)

        self.lay_KL.nextRow()
        self.lay_stock = pg.GraphicsLayout()
        self.lay_stock.setZValue(0)
        self.lay_stock.setFixedHeight(80)
        self.open_label = self.lay_stock.addLabel(u"开盘价", justify="left")
        self.close_label = self.lay_stock.addLabel(u"收盘价", justify="left")
        self.high_label = self.lay_stock.addLabel(u"最高价", justify="left")
        self.low_label = self.lay_stock.addLabel(u"最低价", justify="left")
        self.lay_stock.nextRow()
        self.chg_label = self.lay_stock.addLabel(u"涨跌幅", justify="left")
        self.weight_label = self.lay_stock.addLabel(u"推荐力度", justify="left")
        self.date_label = self.lay_stock.addLabel(u"入选日期", justify="left")

        self.lay_KL.addItem(self.lay_stock)
        # 设置横坐标
        # 初始化子图
        self.init_kline_plot()
        # self.initplotVol()
        # self.initplotOI()
        # 注册十字光标
        # self.crosshair = Crosshair(self.pw,self)
        # 设置界面
        self.vb = QVBoxLayout()
        self.vb.addWidget(self.pw)
        self.setLayout(self.vb)

        self.init_completed = True

    def load_data(self, ts_code):
        if ts_code is not None:
            stock = pd.merge(
                pd.read_sql(
                    sql="select * from stock_daily_tab where ts_code='%s' order by trade_date" % ts_code, con=engine())[["ts_code", "open", "close", "low", "high", "pct_chg", "trade_date"]],
                pd.read_sql(
                    sql="select * from short_stock_pool_tab where ts_code='%s' and delete_status=0" % ts_code,
                    con=engine())[["ts_code", "name", "weight", "count", "level"]],
                on="ts_code")

            self.stock = stock
            
            self.axisTime.update_xdict(dict(enumerate(self.stock["trade_date"].tolist())))

    def refresh_all(self, redraw=True, update=False):
        self.plot_all(redraw, 0, len(self.stock))
        # if not update:
        #     self.update_all()

    def init_kline_plot(self):
        self.pwKL = self.makePI('kline')
        self.candle = CandleStickItem(self.stock)
        self.pwKL.addItem(self.candle)

        self.lay_KL.nextRow()
        self.lay_KL.addItem(self.pwKL)

    def makePI(self, name):
        """生成PlotItem对象"""
        vb = pg.ViewBox()
        plot_item = pg.PlotItem(viewBox=vb, name=name, axisItems={'bottom': self.axisTime})
        plot_item.setMenuEnabled(False)
        plot_item.setClipToView(True)
        plot_item.hideAxis('left')
        plot_item.showAxis('right')
        plot_item.setDownsampling(mode='peak')
        plot_item.setRange(xRange=(0, 1), yRange=(0, 1))
        plot_item.getAxis('right').setWidth(30)
        plot_item.getAxis('right').setStyle(tickFont=QFont("Roman times", 10, QFont.Bold))
        plot_item.getAxis('right').setPen(color=(255, 0, 0, 255), width=0.8)
        plot_item.showGrid(True, True)
        plot_item.hideButtons()
        return plot_item

    def plot_all(self, redraw=True, x_min=0, x_max=11):
        """
        重画所有界面
        redraw ：False=重画最后一根K线; True=重画所有
        xMin,xMax : 数据范围
        """
        self.set_title()
        self.set_stock_info()

        x_max = len(self.stock) - 1 if x_max < 0 else x_max
        y_min = self.stock["open"].min() * 0.8
        y_max = self.stock["open"].max() * 1.2
        self.pwKL.setLimits(xMin=x_min, xMax=x_max, yMin=y_min, yMax=y_max)
        self.plot_kline(redraw, x_min, x_max)

    def plot_kline(self, redraw=False, x_min=0, x_max=-1):
        """
        重画K线子图
        """
        p = self.candle.generatePicture(self.stock, redraw)
        self.candle.paint(p)

    def set_title(self):
        latest_data = self.stock.iloc[-1].to_dict()
        color = 'FF0000'
        if latest_data.get("pct_chg") < 0:
            color = '00FF00'
        self.KLtitle.setText(latest_data.get("ts_code") + "     " + latest_data.get("name"),
                             size='16pt', color=color)

    def set_stock_info(self):
        latest_data = self.stock.iloc[-1].to_dict()
        color = 'FF0000'
        if latest_data.get("pct_chg") < 0:
            color = '00FF00'
        self.open_label.setText("开盘价:      " + str(latest_data.get("open")),
                                size='12pt', color=color)
        self.close_label.setText("收盘价:     " + str(latest_data.get("close")),
                                 size='12pt', color=color)
        self.high_label.setText("最高价:     " + str(latest_data.get("high")),
                                 size='12pt', color=color)
        self.low_label.setText("最低价:     " + str(latest_data.get("low")),
                                 size='12pt', color=color)
        self.chg_label.setText("涨跌幅:     " + str(latest_data.get("pct_chg")),
                                 size='12pt', color=color)
        self.weight_label.setText("推荐力度:     " + str(latest_data.get("count")) + "-" + str(latest_data.get("weight")),
                                 size='12pt', color=color)
        self.date_label.setText("入选日期:     " + str(latest_data.get("trade_date")),
                                 size='12pt', color=color)