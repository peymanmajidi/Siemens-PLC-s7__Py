import snap7
import subprocess
import time as t
import pyodbc
import threading

city = 1



plc = snap7.client.Client()
plc.connect('192.168.2.100', 0, 1)

me = 0
last = 0
lastsub = 0

zero = bytearray(4)
plc.db_write(1,0,zero)

while True:
    temp = plc.db_read(1,0,4)               # DB1.DBD0 
    counter = snap7.util.get_int(temp,2)    # Convert to int
    temp = plc.db_read(1,4,4)               # DB1.DBD4
    maincounter = snap7.util.get_int(temp,2)# Convert to int
    temp = plc.db_read(1,8,2)               # DB1.DBX8.0
    bit = snap7.util.get_int(temp,0)        
    bit = bit > 0                          # Convert to bit
 
    if last == counter:
        continue


    now = t.time()
    last = counter


    me += 1

    if me > 1000: 
        me = 1
    sub = counter - me
    if sub != lastsub:
        print("boom!!")
        lastsub = sub
    
    future = t.time()
    stopwatch = future - now
    print(f"PLC:{counter}\t\tPC:{me}\t\tsub:{sub}\t\t   time={stopwatch:.5f}ms \r", end='', flush= True)

    # print(f"counter:{counter}           main:{maincounter}             bit:{bit}    \r ", end='', flush=True)



