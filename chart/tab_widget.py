# -*- coding: utf-8 -*-
from qtpy.QtWidgets import QTabWidget, QWidget, QHBoxLayout
from pyqtgraph.Qt import QtCore, QtGui

from chart.short_stock_widget import ShortStockPoolWidget
from chart.trend_stock_widget import TrendStockPoolWidget

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class TabWidget(QWidget):
    def __init__(self, *arg):
        super(TabWidget, self).__init__(*arg)
        self.vb = None
        self.tabWidget = None
        self.short_stock_tab = None
        self.trend_stock_tab = None
        self.initUI()

    def _on_click(self, index):
        # if index == 0:
        #     self._refresh_kline()
        # elif index == 1:
        #     self._refresh_real_time()
        pass

    def initUI(self):
        self.vb = QHBoxLayout()

        self.tabWidget = QTabWidget()
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(size_policy)
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)

        self.short_stock_tab = ShortStockPoolWidget()
        self.short_stock_tab.setObjectName(_fromUtf8("short_stock_tab"))
        self.tabWidget.addTab(self.short_stock_tab, _fromUtf8("短线股"))

        self.trend_stock_tab = TrendStockPoolWidget()
        self.trend_stock_tab.setObjectName(_fromUtf8("trend_stock_tab"))
        self.tabWidget.addTab(self.trend_stock_tab, _fromUtf8("趋势股"))

        self.tabWidget.tabBarClicked.connect(self._on_click)

        self.vb.addWidget(self.tabWidget)
        self.setLayout(self.vb)

        self.setStyleSheet('''
        QTabWidget::tab-bar {
            alignment: left;
        }''')

    # def _refresh_kline(self):
    #     print("refresh_kline", self.ts_code)
    #     self.kline_tab.load_data(self.ts_code)
    #     self.kline_tab.refresh_all()
    #
    # def _refresh_real_time(self):
    #     print("refresh_real_time", self.ts_code)
    #     self.real_time_tab.load_data(self.ts_code)
    #     self.real_time_tab.refresh_all()
    #
    # def set_stock_code(self, ts_code):
    #     self.ts_code = ts_code
    #     if self.tabWidget.currentIndex() == 0:
    #         self._refresh_kline()
    #     elif self.tabWidget.currentIndex() == 1:
    #         self._refresh_real_time()

