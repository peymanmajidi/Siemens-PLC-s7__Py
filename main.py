import socket
import pyodbc
import subprocess as shell
import snap7
import time as t
import threading
import datetime
from config import *
import interface

interface.Logo()
print(f"Connecting to database ({DATABASE_IP})...")
db = pyodbc.connect(driver="{FreeTDS}", server=DATABASE_IP, port=1433,
                    database=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD)
print("Connected.")
cursor = db.cursor()
plc = snap7.client.Client()
plc.connect(PLC_IP, 0, 1)


def Select(table, keyword, key):
    global db
    cursor = db.cursor()
    q = f"SELECT * FROM {table} WHERE {keyword}='{key}'"
    cursor.execute(q)
    data = cursor.fetchall()
    if len(data) > 0:
        return True, data[0]
    return False, None


def Insert(table, cols, values):
    global db
    try:
        insert_query = f"""INSERT INTO {table} ({cols}) 
        VALUES({values})"""
        cursor.execute(insert_query)
        db.commit()
        return True
    except:
        return False


def TCP_Listener():
    row_number = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST_IP, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f'Connected to {addr}')
                interface.Init()
                while True:
                    row_number += 1
                    city = REJECT_TITLE
                    barcode = NO_BARCODE
                    gate = REJECT_GATE
                    datalogic_back = conn.recv(1024).decode()
                    datalogic_back = str(datalogic_back).upper().replace(
                        "\r\n", "").replace("\x02", "")
                    if len(datalogic_back) > 3:  # something happend ------------------------------
                        sortTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if DATALOGIC_NO_READ in datalogic_back:
                            pass
                        else:
                            success, excel = Select(
                                table="ImportsTBL", keyword="barcode", key=datalogic_back)
                            if success:
                                city = excel.city
                                success, gate_def = Select(
                                    table="GateDefsTBL", keyword="city", key=city)
                                if success:
                                    gate = gate_def.gateNumber
                                barcode = datalogic_back
                            else:  # mazad
                                city = "NO EXCEL(Rj)"
                                barcode = datalogic_back

                        success = Insert(table="GateParcelsListTBL",
                               cols="gatedefid,barcode,[timestamp],gatenumber", values=f"{gate},'{barcode}','{sortTime}',{gate}")
                        interface.Print_Row(
                            i=row_number, gate=gate, city=city, barcode=barcode, sortTime=sortTime)
                        plc.db_write(1, 0, bytearray([0, 0, 0, gate]))
                    # ------------------------------------------------------------------------
        except OSError:
            print("Service is running...")
            print("First stop it then try again")


try:
    print("Press Ctrl+C to stop the service")
    TCP_Listener()
except KeyboardInterrupt:
    print()
    print("Service Stopped.")
    print("Happy go lucky :)")
