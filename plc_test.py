import snap7


plc = snap7.client.Client()
plc.connect('192.168.2.100', 0, 1)

me = 0
last = 0
lastsub = 0


plc.db_write(1,0, bytearray([0,0,0,44]))
# pause = input("press enter...")
temp = plc.db_read(1,0,4)               # DB1.DBD0 
counter = snap7.util.get_int(temp,2)    # Convert to int
print(counter)
