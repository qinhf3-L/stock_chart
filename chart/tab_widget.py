# -*- coding: utf-8 -*-
from qtpy.QtWidgets import QTabWidget, QWidget, QHBoxLayout
from pyqtgraph.Qt import QtCore, QtGui


from chart.kline_widget import KLineWidget
from chart.real_time_widget import RealTimeWidget

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class TabWidget(QWidget):
    def __init__(self, ts_code, *arg):
        super(TabWidget, self).__init__(*arg)
        self.vb = None
        self.tabWidget = None
        self.real_time_tab = None
        self.kline_tab = None
        self.ts_code = ts_code
        self.initUI()

    def _on_click(self, index):
        if index == 0:
            self._refresh_kline()
        elif index == 1:
            self._refresh_real_time()

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

        self.kline_tab = KLineWidget(self.ts_code)
        self.kline_tab.setObjectName(_fromUtf8("kline_tab"))
        self.tabWidget.addTab(self.kline_tab, _fromUtf8("日K线"))

        self.real_time_tab = RealTimeWidget(self.ts_code)
        self.real_time_tab.setObjectName(_fromUtf8("real_time_tab"))
        self.tabWidget.addTab(self.real_time_tab, _fromUtf8("分时图"))

        self.tabWidget.tabBarClicked.connect(self._on_click)

        self.vb.addWidget(self.tabWidget)
        self.setLayout(self.vb)

        self.setStyleSheet('''
        QTabWidget::tab-bar {
            alignment: left;
        }''')

    def _refresh_kline(self):
        print("refresh_kline", self.ts_code)
        self.kline_tab.load_data(self.ts_code)
        self.kline_tab.refresh_all()

    def _refresh_real_time(self):
        print("refresh_real_time", self.ts_code)
        self.real_time_tab.load_data(self.ts_code)
        self.real_time_tab.refresh_all()

    def set_stock_code(self, ts_code):
        self.ts_code = ts_code
        if self.tabWidget.currentIndex() == 0:
            self._refresh_kline()
        elif self.tabWidget.currentIndex() == 1:
            self._refresh_real_time()

