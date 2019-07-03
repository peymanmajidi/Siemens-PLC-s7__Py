import snap7

client = snap7.client.Client() # before running this line you should run this command only first time: sudo ldconfig
client.connect('192.168.2.180', 0, 1)

m =  client.db_read(10,8,4)
client.db_write(10,8,u) # DB10.DBW2


