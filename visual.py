import snap7
import subprocess
import time as t
import pyodbc
import threading
import logo

city = 1
logo.print_logo()


def database():
    # global city
    # cnxn = pyodbc.connect(driver = "{FreeTDS}", server = "192.168.2.82", port = 1433, database="prototypedb", user="sa", password="server@1314")
    # cursor = cnxn.cursor()
    t.sleep(2)

    # query = f"SELECT * FROM [BarcodesTBL] where how  = {0}"
    # cursor.execute(query)
    # barcode = cursor.fetchall()[0]
    # city+=1
    # cursor.execute(f"insert into ParcelsTBL values( '{barcode.barcode}','{city}',{counter})")
    # cnxn.commit()


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
    print("▄▄", end='')
    if last == counter:
        continue


    now = t.time()
    last = counter

    x = threading.Thread(target=database)
    x.start()

    me += 1

    if me > 1000: 
        me = 1
    sub = counter - me
    
    future = t.time()
    stopwatch = future - now
    if sub != lastsub:
        print(f" ::::::: WRONG :::::{stopwatch:.5f}")
        lastsub = sub
    else:
        print(f"{stopwatch:.5f}")
    # print(f"\r\nPLC:{counter}\t\tPC:{me}\t\tsub:{sub}\ttime={stopwatch:.5f}ms")
    # print(f"counter:{counter}           main:{maincounter}             bit:{bit}    \r ", end='', flush=True)



