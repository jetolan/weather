
import time
import board
import busio
import adafruit_ina219

i2c = busio.I2C(board.SCL, board.SDA)
ina219 = adafruit_ina219.INA219(i2c)

while True:
 BV=ina219.bus_voltage
 SV=ina219.shunt_voltage / 1000
 I=ina219.current
 
 print("Shunt = "+str(SV)+"V, Bus = "+str(BV)+\
       "V , Current = "+str(I)+"mA, Power = "+str(BV*I)+"mW")
 time.sleep(.5)
