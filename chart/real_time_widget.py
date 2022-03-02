import pyqtgraph as pg
import pandas as pd
from qtpy.QtWidgets import QWidget, QVBoxLayout

from db.db import engine


class RealTimeWidget(QWidget):

    def __init__(self, ts_code=None):
        """Constructor"""
        super(RealTimeWidget, self).__init__()
        self.vb = QVBoxLayout()
        self.initUI()

    def initUI(self):
        """初始化界面"""
        self.setWindowTitle(u'K线工具')
        # 主图
        self.pw = pg.PlotWidget()
        # 界面布局
        self.lay_KL = pg.GraphicsLayout(border=(100,100,100))
        self.lay_KL.setContentsMargins(10, 10, 10, 10)
        self.lay_KL.setSpacing(0)
        self.lay_KL.setBorder(color=(255, 0, 0, 255), width=0.8)
        self.lay_KL.setZValue(0)
        self.KLtitle = self.lay_KL.addLabel(u'')
        self.pw.setCentralItem(self.lay_KL)
        # 设置横坐标
        xdict = {}
        # self.axisTime = MyStringAxis(xdict, orientation='bottom')
        # 初始化子图
        # self.initplotKline()
        # self.initplotVol()
        # self.initplotOI()
        # 注册十字光标
        # self.crosshair = Crosshair(self.pw,self)
        # 设置界面
        self.vb = QVBoxLayout()
        self.vb.addWidget(self.pw)
        self.setLayout(self.vb)
        # 初始化完成
        self.initCompleted = True

    def load_data(self, ts_code):
        pass
        # if ts_code is not None:
        #     self.stock = pd.read_sql(
        #         sql="select * from real_time_stock_tab where ts_code='%s' order by trade_time" % ts_code,
        #         con=engine())
        #     latest_data = self.stock.iloc[-1].to_dict()
        #     color = 'FF0000'
        #     if latest_data.get("pct_chg") < 0:
        #         color = '00FF00'
        #     self.KLtitle.setText(latest_data.get("ts_code") + "     " + latest_data.get("name"),
        #                          size='16pt', color=color)

    def refresh_all(self):
        pass
