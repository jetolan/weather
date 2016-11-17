from subfact_pi_ina219 import Subfact_ina219
import time

while True:
 ina=Subfact_ina219.INA219()
 BV=ina.getBusVoltage_V()
 SV=ina.getShuntVoltage_mV()
 I=ina.getCurrent_mA()
 print "Shunt = "+str(SV)+"V, Bus = "+str(BV)+\
       "V , Current = "+str(I)+"mA, Power = "+str(BV*I)+"mW"
 time.sleep(.5)
