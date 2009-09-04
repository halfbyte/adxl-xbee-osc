#!/usr/bin/python
#
import serial, time, osc
from xbee import xbee

SERIALPORT = "/dev/tty.usbserial-FTDPYKW9"

BAUDRATE = 9600 

# open up the FTDI serial port to get data transmitted to xbee
ser = serial.Serial(SERIALPORT, BAUDRATE)
ser.open()
osc.init()


i = 0
while 1:
    packet = xbee.find_packet(ser)
    if packet:
        i = i+1
        xb = xbee(packet)
        voltage = xb.analog_samples[0][3] * 0.0064
        x = xb.analog_samples[0][2]
        y = xb.analog_samples[0][1]
        z = xb.analog_samples[0][0]
        
        if i % 100 == 0:
          osc.sendMsg("/voltage/%d" % (xb.address_16), [voltage])
          print "voltage: %f" % (voltage)
        
        osc.sendMsg("/accxyz/%d" % (xb.address_16), [x,y,z])
