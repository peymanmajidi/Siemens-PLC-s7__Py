import snap7

plc = snap7.client.Client()
plc.connect('192.168.2.100', 0, 1)

me = bytearray(b'\x00\x05')
plc.db_write(1,2,me)

while 1:
    temp = plc.db_read(1,2,2) # DB1.DBD0
    counter = snap7.util.get_int(temp,0)
    temp = plc.db_read(1,6,2) # DB1.DBD4
    maincounter = snap7.util.get_int(temp,0)
    temp = plc.db_read(1,8,1)
    bit = snap7.util.get_bool(temp,0,1)  # DB1.DBX8.0
    
    print(f"counter:{counter}\tmain:{maincounter}\tbit:{bit}")




