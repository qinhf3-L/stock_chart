import pandas as pd
import pyqtgraph as pg
from qtpy import QtWidgets
from qtpy.QtWidgets import QWidget, QTreeWidget, QHBoxLayout

from chart.short_kline_widget import ShortKLineWidget
from db.db import engine


class ShortStockPoolWidget(QWidget):

    def __init__(self, parent=None):
        super(ShortStockPoolWidget, self).__init__(parent)
        self.stocks_daily = None
        self.stocks = None
        self.concept_stocks = None
        self.concepts = None
        self.current_ts_code = None
        self.vb = QHBoxLayout()
        self.splitter = QtWidgets.QSplitter()
        self.kline_pw = None
        self.tree = None
        self.load_data_from_sql()
        self.initUI()

    def _on_tree_click(self, item):
        if item.childCount() == 0:
            self.kline_pw.load_data(item.text(1))
            self.kline_pw.refresh_all()

    def initUI(self):
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self._refreshTree()
        self.tree.itemClicked.connect(self._on_tree_click)

        self.kline_pw = ShortKLineWidget(self.current_ts_code)

        self.splitter.addWidget(self.tree)
        self.splitter.addWidget(self.kline_pw)

        self.vb.addWidget(self.splitter)
        self.setLayout(self.vb)
        self.resize(1600, 900)

    def _refreshTree(self):
        head_item = None
        item = pg.TreeWidgetItem(["短线股", "1", "1", "1"])
        self.tree.addTopLevelItem(item)
        short_stocks = pd.read_sql(
            sql="select * from short_stock_pool_tab where delete_status = 0 order by count desc, weight desc",
            con=engine())

        for i, stock_row in short_stocks.iterrows():
            sub_item = pg.TreeWidgetItem(
                [stock_row["name"], stock_row["ts_code"], str(stock_row["weight"]),
                 str(stock_row["level"])])
            if head_item is None:
                head_item = sub_item
            item.addChild(sub_item)

        for i, concept_row in self.concepts.iterrows():
            group = pd.merge(
                self.concept_stocks[self.concept_stocks["concept_name"] == concept_row["concept_name"]],
                self.stocks, on=["symbol"])
            if len(group) > 3:
                group.sort_values(by=["level", "weight"], ascending=[False, False], inplace=True)
                item = pg.TreeWidgetItem(
                    [concept_row["concept_name"], str(concept_row["count"]), str(concept_row["weight"]),
                     str(concept_row["pct_chg"])])
                self.tree.addTopLevelItem(item)
                for j, stock_row in group.iterrows():
                    sub_item = pg.TreeWidgetItem(
                        [stock_row["name"], stock_row["ts_code"], str(stock_row["weight"]), str(stock_row["level"])])
                    item.addChild(sub_item)

        self.tree.setCurrentItem(head_item)
        self.current_ts_code = head_item.text(1)

    def load_data_from_sql(self):
        self.concepts = pd.read_sql(sql="select * from concept_pool_tab where delete_status=0", con=engine())
        self.concepts.sort_values(by=["count", "weight", "pct_chg"], ascending=[False, False, False], inplace=True)
        self.concept_stocks = pd.read_sql(sql="select * from concept_stocks_tab", con=engine())
        self.stocks = pd.read_sql(sql="select * from short_stock_pool_tab where delete_status = 0", con=engine())
