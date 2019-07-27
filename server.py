import socket
import pyodbc
import subprocess as shell
import snap7
import time as t
import threading
import datetime

HOST = '192.168.2.75'  # Standard loopback interface address (localhost)
PORT = 2020             # Port to listen on (non-privileged ports are > 1023)
REJECT = 24

# Specifying the ODBC driver, server name, database, etc. directly
print("Connecting...")
cnxn = pyodbc.connect(driver = "{FreeTDS}", server = "192.168.2.41", port = 1433, database="prototypedb", user="sa", password="server@1314")
print("Connected")
cursor = cnxn.cursor()


plc = snap7.client.Client()
plc.connect('192.168.2.100', 0, 1)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try: 
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                city = "Reject"
                barcode = "< NO DATA >"
                gate = REJECT
                datalogic_back = conn.recv(1024).decode()
                datalogic_back= str(datalogic_back).upper().replace("\r\n","").replace("\x02","")
                if len(datalogic_back) > 3: # something happend ------------------------------
                    sortTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if "NO READ" in datalogic_back:
                        pass
                    else:
                        cursor = cnxn.cursor()
                        q = f"SELECT * FROM dbo.ImportsTBL WHERE barcode='{datalogic_back}'"
                        cursor.execute(q)
                        row = cursor.fetchall()
                        if len(row) > 0:
                            gate = row[0].gate
                            city = row[0].city
                            barcode = datalogic_back
                        else: # mazad
                            gate = REJECT
                            city = "No Where"
                            barcode = datalogic_back

    
                    cursor.execute(f"INSERT INTO dbo.GateListTBL VALUES({gate},'{barcode}','{sortTime}')")
                    cnxn.commit()
                    print(f"city: {city}({gate})\tbarcode: {barcode}\tTime: {sortTime}")
                    plc.db_write(1,0, bytearray([0,0,0, gate]))
                # ------------------------------------------------------------------------
                
    except OSError:
        print("Program is running...")
        print("First stop it, try again")



