import time
import snap7
# from snap7 import util

def write(client, n):
    
    u = hex(n)
    print(u)
    j = len(u)
    f = str(u)[2:]

    for i in range(10-len(u)):
        f="0" + f
    
    u = bytearray(4)
    ff = f[0:2]
    u[0] = int(f[0:2],16)
    u[1] = int(f[2:4],16)
    u[2] = int(f[4:6],16)
    u[3] = int(f[6:8],16)
    print(u)
    client.db_write(10,8,u) # DB10.DBW2

client = snap7.client.Client()
client.connect('192.168.2.180', 0, 1)
last = -1

write(client, 0)



while True:
    m =  client.db_read(10,8,4)
    if m != last:
        print("orgin:\t" , m)
        cat = ""
        if len(m) > 0:
            for i in m:

                h = hex(i) 
                if i > 15:
                    cat =cat + h[2] + h[3]
                else:
                    cat =cat + "0" + h[2]
        
        if cat == '':
            cat = '0x00'
        print("cat:\t",cat)
        print(int(cat,16))

        last = m



print("ok")