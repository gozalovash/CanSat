import sys
import serial
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import pyqtgraph as pg


# implement serial here somehow

def reset():
    s = serial.Serial('COM6', 115200)
    data_to_reset = "0"
    s.write(data_to_reset.encode('utf-8'))
    s.close()


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # ComboBox
        cbox = QComboBox()
        cbox.addItem('COM6')
        cbox.addItem('COM2')

        # BUTTONS
        # RESET
        btn = QPushButton('Reset')
        btn.resize(btn.sizeHint())
        btn.clicked.connect(reset())

        # Show
        sbtn = QPushButton('Select Port')
        sbtn.resize(btn.sizeHint())

        # TABLE
        table = QTableWidget()
        table.setFixedSize(270, 90)
        table.setColumnCount(4)
        table.setRowCount(2)
        table.setHorizontalHeaderLabels(["Temperature", "Speed", "Altitude", "Pressure"])
        for i in range(2):
            for j in range(4):
                table.setItem(i, j, QTableWidgetItem("1"))
        table.resizeColumnsToContents()

        # GRAPH
        graph = pg.PlotWidget()
        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 40]

        # plot data: x, y values
        graph.plot(hour, temperature)
        graph.setXRange(0, 10)
        graph.setYRange(27, 40)

        #  LAYOUT
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox1.addWidget(cbox)
        hbox1.addWidget(sbtn)
        hbox2.addWidget(btn)
        hbox3.addWidget(graph)

        vbox = QVBoxLayout()
        # vbox.setSpacing(30)
        # vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(table)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)

        # WINDOW SIZE AND POSITION
        self.resize(600, 400)
        self.center()
        self.setWindowTitle('CanSat Base Station')
        self.setWindowIcon(QIcon('candy.jpg'))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Door',
                                     "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
