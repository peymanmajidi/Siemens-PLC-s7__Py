import snap7

plc = snap7.client.Client()
plc.connect('192.168.2.100', 0, 1)


while 1:
    temp = plc.db_read(1,0,4)               # DB1.DBD0 
    counter = snap7.util.get_int(temp,2)    # Convert to int
    temp = plc.db_read(1,4,4)               # DB1.DBD4
    maincounter = snap7.util.get_int(temp,2)# Convert to int
    temp = plc.db_read(1,8,2)               # DB1.DBX8.0
    bit = snap7.util.get_int(temp,0)     # Convert to bit
    bit = bit > 0
    print(f"counter:{counter}\tmain:{maincounter}\tbit:{bit}")


