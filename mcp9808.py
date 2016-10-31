import smbus
import time



#find the address of MCP9808 using
#$i2cdetect -y 1
#where the 1 at the end is pi model specific (try 0)
bus=smbus.SMBus(1) #1 corresponds to above
address=0x18

#these values from
#MCP9808 datasheet
temp_reg=0x5
res_reg=0x8

#bus.write_byte(address,temp_reg)
#value=bus.read_byte_data(address, temp_reg)
#value=bus.read_word_data(address, temp_reg)
reading = bus.read_i2c_block_data(address, temp_reg)
t = (reading[0] << 8) + reading[1]

def temp_c(data):
 temp= (data & 0xFFF) / 16.0

 if data & 0x1000:
   temp-=256
 return temp    

print temp_c(t)

