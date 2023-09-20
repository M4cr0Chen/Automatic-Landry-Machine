import time
from pyb import Servo
from pyb import UART
s1 = Servo(1)
s2 = Servo(2)
s3 = Servo(3)
uart = UART(3, 9600)
uart.init(9600, bits=8, parity=None, stop=1)
while (True):
    if uart.any():
        tmp_data = uart.readline()
        print(tmp_data)
        s1.pulse_width(1000)
        s2.pulse_width(1000)
        s3.pulse_width(1900)
        if tmp_data.decode().startswith(b'111'):
            s1.pulse_width(1900)
            s2.pulse_width(1000)
            s3.pulse_width(1000)
            time.sleep(2000)
        if tmp_data.decode().startswith(b'222'):
            s1.pulse_width(1000)
            s2.pulse_width(1900)
            s3.pulse_width(1000)
            time.sleep(2000)
    time.sleep(1000)
