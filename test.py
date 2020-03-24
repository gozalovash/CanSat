import sys
from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QDesktopWidget)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('Sanserif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        # BUTTONS
        btn = QPushButton('Candy', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(30, 30)

        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(30, 70)
        qbtn.setToolTip('Tap to quit')

        # WINDOW SIZE AND POSITION
        self.resize(250, 150)
        self.center()
        self.setWindowTitle('Candy Shop')
        self.setWindowIcon(QIcon('candy.jpg'))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Door',
                                     "Are you sure to quit our Candy Heaven?",
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
