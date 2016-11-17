import time
import Adafruit_ADS1x15
import matplotlib.pyplot as plt

# Create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1015()

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN =4

# Read the difference between channel 0 and 1 (i.e. channel 0 minus channel 1).
# Note you can change the differential value to the following:
#  - 0 = Channel 0 minus channel 1
#  - 1 = Channel 0 minus channel 3
#  - 2 = Channel 1 minus channel 3
#  - 3 = Channel 2 minus channel 3
plt.axis([0,100,-1000,1000])
plt.ion()
i=0
values=[]
while True:
#    val=[adc.read_adc(0, gain=GAIN), \
#         adc.read_adc(1, gain=GAIN), \
#         adc.read_adc(2, gain=GAIN), \
#         adc.read_adc(3, gain=GAIN), \
#        ]
     val = adc.read_adc_difference(0, gain=GAIN)
     plt.scatter(i, val)
     values.append(val)
     i=i+1
     plt.pause(0.1)
     #time.sleep(0.05)

