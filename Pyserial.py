import serial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for p in ports:
    # print(p)
    print(p.device)
# to get data
s = serial.Serial('COM6', 115200)
while (True):
    res = s.readline().decode('utf-8')
    print(res)
