import pyqtgraph as pg

# Press the green button in the gutter to run the script.
from chart.short_stock_widget import StockPoolWidget

if __name__ == '__main__':
    app = pg.mkQApp("")

    splitter = StockPoolWidget()
    splitter.show()

    pg.exec()
