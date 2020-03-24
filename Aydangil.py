import serial

"""
#to check the open ports
import seria.ltools.list_ports
ports = serial.tools.list_ports.comports()
for p in ports:
    #print(p)
    print(p.device)
#to get data
s = serial.Serial('COM6',115200)
while(True):
    res = s.readline().decode('utf-8')
    print(res)
"""
import _sqlite3
import csv
import time
from datetime import datetime
import random

"""from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count   #for live graph
import pandas   #for live graph, installed
from matplotlib import style
import animate"""
# import os   ???
# difference between time and datetime

connection = _sqlite3.connect("practice.db")  # creates connetion to a database
cursor = connection.cursor()  # creates a cursor object to interact


def create_table():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS dataToPlot(height1 REAL, time1 REAL)")  # dataToPlot is the name of the table that we create


def data_entry():
    strng = "001,2,3,97.03,499.85,10.00,36.01,40.00,0,1000,0,0,0,"
    s = serial.Serial('COM6', 115200)
    x = 5
    j = 0
    while (x > 0):
        data = s.readline().decode('utf-8')
        pr = data.split(",")
        var1 = float(pr[6])
        var2 = float(pr[9])
        cursor.execute("INSERT INTO dataToPlot (height1, time1) VALUES (?, ?)", (var1, var2))
        connection.commit()  # saves to database
        cursor.execute("SELECT * FROM dataToPlot LIMIT 1 OFFSET (?)", (int(j)))
        res = cursor.fetchall()
        print(res)
        x -= 1
        j += 1


def dynamic_data_entry():
    '''   does not work
    for i in range (4, 10):
        j = 10*i
        cursor.execute("""INSERT INTO dataToPlot VALUES(int(i*10), int(i)""")   #why not j
        time.sleep(5)
    connection.commit()
    '''
    # now: datetime = datetime.now()   #shows current time (time.time and now difference?)
    # take the start time 0 and continue x seconds and enter data dynamically for example every 2 seconds and
    # graph it simultaneously   ???time.time; sleep(x); time.time   ???
    hght = random.randrange(10, 100)
    for i in range(3, 10):
        cursor.execute("INSERT INTO dataToPlot (height1, time1) VALUES (?, ?)",
                       (int(hght), int(i)))  # for inserting variables
        connection.commit()
        time.sleep(2)
    # connection.commit()
    # but the graph will be shown after the loop is finished, not simultaneously


def print_table():  # just its data
    cursor.execute("SELECT * FROM dataToPlot")
    # print(cursor.fetchall())
    res = cursor.fetchall()
    for j in res:
        print(j)
        time.sleep(1)
    connection.commit()


def clear_database():
    cursor.execute("DELETE from dataToPlot")
    connection.commit()


def data_to_csv():
    with open("practice.csv", "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])
        # csv_writer.writerows(cursor)
        cursor.execute("SELECT * FROM dataToPlot")
        res = cursor.fetchall()
        for j in res:
            csv_writer.writerow(j)


def clear_csvfile():
    pass  # how to clear csv file


def data_to_plot():  # not for dynamic
    cursor.execute("SELECT * FROM dataToPlot")
    data = cursor.fetchall()
    height = []
    time = []
    for row in data:
        height.append(row[0])
        time.append(row[1])
    # plt.cla()
    plt.plot(height, time)
    plt.style.use("fivethirtyeight")  # ???
    # modify the design of the graph
    # print(plt.style.available())
    plt.tight_layout()  # ???  automatic padding
    plt.show()


# anmte = FuncAnimation(plt.gcf(), animate, interval = 2000)   #2 seconds   #there is a problem with animate in the background
# gcf - get current figure
def live_graph():
    pass


# dynamic data entry
# dynamically writing to csv file
# sliding the graph while new values are being added
# printing the data in the form of table
# customizing the graph (size, numbers, size and so on)

if __name__ == '__main__':
    create_table()
    data_entry()
    # dynamic_data_entry()
    # clear_database()
    # print_table()
    # clear_csvfile()
    # data_to_csv()
    # data_to_plot()

    cursor.close()
    connection.close()
"""
#to check the open ports
import seria.ltools.list_ports
ports = serial.tools.list_ports.comports()
for p in ports:
    #print(p)
    print(p.device)
x=6
while(x>0):
    a=input()
    s.write(a.encode())
    x=x-1"""
