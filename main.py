import socket
import pyodbc
import subprocess as shell
import snap7
import time as t
import threading
import datetime
import Modules.logo as logo

HOST = '192.168.2.75'  # Standard loopback interface address (localhost)
PORT = 2020            # Port to listen on (non-privileged ports are > 1023)
REJECT = 24
row_number = 0
logo.print_logo()
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
            print("""
┌───────┬──────────────────┬─────────────────────────┬──────────────┬───────────────────────┐
│  #    │       CITY       │          BARCODE        │     GATE     │      TIME STAMP       │
├───────┼──────────────────┼─────────────────────────┼──────────────┼───────────────────────┤
└───────┴──────────────────┴─────────────────────────┴──────────────┴───────────────────────┘\r""",end = '')

            while True:
                row_number+=1
                city = "Reject"
                barcode = "** NO BARCODE **"
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
                        excel = cursor.fetchall()
                        if len(excel) > 0:
                            city = excel[0].city
                            q = f"SELECT * FROM dbo.GateDefsTBL WHERE city='{city}'"
                            cursor.execute(q)
                            gate_def = cursor.fetchall()
                            if len(gate_def) > 0:
                                gate = gate_def[0].gateNumber
                            barcode = datalogic_back
                        else: # mazad
                            city = "NO EXCEL(Rj)"
                            barcode = datalogic_back

                    insert_query = f"""INSERT INTO dbo.GateParcelsListTBL (gatedefid,barcode,[timestamp],gatenumber) 
                     VALUES({gate},'{barcode}','{sortTime}',{gate})"""
                    cursor.execute(insert_query)
                    cnxn.commit()
                    gate_str = str(gate) if gate >9 else "0" + str(gate)
                    row = f"│  #    │       CITY       │          BARCODE        │     GATE     │      TIME STAMP       │"
                    row = row[:2] + str(row_number) + ((5-len(str(row_number)))* ' ') + row[7:]
                    row = row[:10] + city + ((17 - len(city))* ' ') + row[27:]
                    row = row[:30] + barcode + ((22 - len(barcode))* ' ') + row[52:]
                    row = row[:59] + gate_str + ((8 - len(gate_str))* ' ') + row[67:]
                    row = row[:71] + sortTime + ((21 - len(sortTime))* ' ') + row[92:]
                    print( row)
                    print("└───────┴──────────────────┴─────────────────────────┴──────────────┴───────────────────────┘\r",end = '')
                    plc.db_write(1,0, bytearray([0,0,0, gate]))
                # ------------------------------------------------------------------------                
    except OSError:
        print("Program is running...")
        print("First stop it, try again")



