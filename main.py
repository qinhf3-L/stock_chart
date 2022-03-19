import pyqtgraph as pg
from chart.tab_widget import TabWidget

if __name__ == '__main__':
    app = pg.mkQApp("")

    splitter = TabWidget()
    splitter.show()

    pg.exec()
