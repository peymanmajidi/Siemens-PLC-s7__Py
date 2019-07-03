# plc_read_write
write and read double word on plc s7

## What you need
wget http://sourceforge.net/projects/snap7/files/1.2.1/snap7-full-1.2.1.tar.gz/download

tar -zxvf snap7-full-1.2.1.tar.gz

cd snap7-full-1.2.1/build/unix && sudo make -f arm_v6_linux.mk all

sudo cp ../bin/arm_v6-linux/libsnap7.so /usr/lib/libsnap7.so

sudo cp ../bin/arm_v6-linux/libsnap7.so /usr/local/lib/libsnap7.so

sudo apt-get install python3-pip

sudo pip3 install python-snap7

## update soon


