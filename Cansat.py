import sys, os, csv
import serial
import serial.tools.list_ports
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import QSize, Qt

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
        btn.clicked.connect(self.temp_reset)  # change this to reset instead of temp_reset

        # Show
        sbtn = QPushButton('Read from Port')
        sbtn.resize(btn.sizeHint())
        sbtn.clicked.connect(self.temp_readPort)  # change to read_port

        self.counter = 0

        # TABLE
        self.table = QTableWidget()
        # table.resize(table.sizeHint())
        self.table.setFixedSize(595, 350)
        self.table.setFont(QFont('Verdana', 6))
        self.table.setWordWrap(True)
        self.table.setColumnCount(13)
        self.table.setRowCount(20)

        for i in range(13):
            self.table.setColumnWidth(i, 43)

        self.table.setHorizontalHeaderLabels(["netID", "Time", "TPS", "Battery Voltage", "Altitude",
                                              "Speed", "Latitude", "Longitude", "Camera stat.", "RPM",
                                              "Drop-time", "Taken Photos", "Sent Photos"])

        # table.resizeColumnsToContents()

        # GRAPH
        self.graph = pg.PlotWidget()
        # graph = pg.plot()
        self.graph.setBackground('w')
        self.graph.setLabel('left', 'Altitude', color='Red', size=35)
        self.graph.setLabel('bottom', 'Time', color='Red', size=35)
        self.graph.resize(200, 200)
        self.graph.setXRange(0, 10)
        self.graph.setYRange(250, 500)
        self.pen = pg.mkPen(color=(255, 0, 0))
        self.x_range = [500]
        self.y_range = [0]

        labelImage2 = QLabel(self)
        pixmap2 = QPixmap('images/icon1.jpg')
        smaller_pixmap2 = pixmap2.scaled(277, 300, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelImage2.setPixmap(smaller_pixmap2)

        # LAYOUT
        h_box1 = QHBoxLayout()
        h_box1.addWidget(cbox)
        h_box1.addWidget(sbtn)
        h_box2 = QHBoxLayout()
        h_box2.addWidget(btn)
        h_box3 = QHBoxLayout()
        h_box3.addWidget(self.table)
        # h_box4 = QHBoxLayout()
        # h_box4.addWidget(graph)
        # h_box4.addWidget(labelImage1)
        h_box5 = QHBoxLayout()

        v_box1 = QVBoxLayout()
        v_box1.addWidget(labelImage2)
        v_box1.addWidget(self.graph)
        # v_box1.addLayout(h_box4)
        v_box2 = QVBoxLayout()
        v_box2.addLayout(h_box1)
        v_box2.addLayout(h_box2)
        v_box2.addLayout(h_box3)

        b_box = QHBoxLayout()
        b_box.addLayout(v_box2)
        b_box.addLayout(v_box1)

        self.setLayout(b_box)

        # WINDOW SIZE AND POSITION
        # self.setMaximumSize(1500, 500)
        self.setFixedSize(900, 440)
        # self.showFullScreen()
        self.center()
        self.setWindowTitle('CanSat Base Station')
        self.setWindowIcon(QIcon('images/candy.jpg'))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def readPort(self):
        ports = serial.tools.list_ports.comports()
        for p in ports:
            # print(p)
            print(p.device)
        # to get data
        s = serial.Serial('COM6', 115200)
        while (True):
            res = s.readline().decode('utf-8')
            print(res)
            self.parseData(res)

    def temp_readPort(self):
        with open('test_input.csv', newline='') as csvfile:
            dummy = csv.reader(csvfile, delimiter=',')
            self.line = 0
            for row in dummy:
                self.parseData(row)

    def parseData(self, old_string):
        new_string = old_string[:-1]
        self.fillTable(new_string)
        self.fillGraph(new_string)
        self.write_string_to_csv(old_string)

    def write_string_to_csv(self, strng):
        with open("output_file.csv", "a", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(strng)
            # csv_writer.writerow([i[0] for i in cursor.description])
            # strng = "001,2,3,97.03,499.85,10.00,36.01,40.00,0,1000,0,0,0,"

            # pr = strng.split(",")
            # csv_writer.writerow(pr)

    def fillTable(self, string):
        for i in range(13):
            self.table.setItem(self.line, i, QTableWidgetItem(string[i]))
            self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignRight)
        self.line += 1

        # table.item(line, i).setTextAlignment(Qt.AlignRight)
        # table.horizontalHeaderItem(i).setDefaultAlignment(Qt::AlignCenter | (Qt::Alignment)Qt::TextWordWrap)

    def fillGraph(self, string):
        self.y_range.append(int(string[1]))
        self.x_range.append(int(string[4]))
        if len(self.x_range) == len(self.y_range):
            self.graph.plot(self.y_range, self.x_range, pen=self.pen)

    def reset(self, counter=0):
        counter += 1
        s = serial.Serial('COM6', 115200)
        data_to_reset = "0"
        s.write(data_to_reset.encode('utf-8'))
        s.close()
        if counter < 2:
            self.clear_csvfile()
            # clear csv file here
        else:
            self.insert_reset_line()
            self.table.clear()
            # clean table and graph here
        print(0)

    def temp_reset(self):
        self.counter += 1
        if self.counter < 2:
            self.clear_csvfile()
            self.table.clearContents()
            self.graph.clear()
            self.x_range = [500]
            self.y_range = [0]
        else:
            # clean table and graph here, insert a line in csv to know when reset was pressed
            self.insert_reset_line()
            self.table.clearContents()
            self.graph.clear()
            self.x_range = [500]
            self.y_range = [0]
        print(0)

    def insert_reset_line(self):
        zero_row = ""
        for i in range (0, 13):
            zero_row += "0"
        with open("output_file.csv", "a", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(zero_row)

    def clear_csvfile(self):
        f = open('output_file.csv', 'w')  # only removes content
        f.truncate()
        f.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
