#!/usr/bin/python

import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
import math
import pymysql.cursors
import struct
import array
import ctypes


##------------------Connect to database-----------------------------##


##
# connect to the database you created with the credentials you set up
connection = pymysql.connect(host='localhost',
    user='root',
    password='root',
    db='ICBP',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
# END CODE


##--------------Collecting Data From Arduino------------------------------##

GPIO.setmode (GPIO.BCM)

#Send and receive addresses
pipe = [[0xE8, 0xE8, 0xF0, 0xF0, 0XE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xB5]]

# Setup Radio
radio = NRF24 (GPIO, spidev.SpiDev())

#begin radio and pass CSN to gpio (8/ce0) and CE to gpio 17
radio.begin(0,17)

#Max bytes 32
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipe[1])
##radio.printDetails()
radio.startListening()

while True:

    while not radio.available(0):
        time.sleep (1)

## Print array
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print ("Received from Arduino: {}".format(receivedMessage))

    
    print str(receivedMessage)[1:-1]
    print ""
    
    
    #Break into two set of 4 bytes
    Volts = (receivedMessage)[0:+4]
    Amps = (receivedMessage)[4:+8]
    print Volts #Print the four bytes that represent voltage value
    print Amps # Print the four bytes that represent current value
    print ""

    #The join line converts each integer value into a character byte
    #then joins them together into a single string which is what
    #the struct.unpack requires as an input
    
    volt = ''.join(chr(i) for i in Volts)
    v = struct.unpack('<f', volt)  # '<' for little-endian
    volts = v[0] # A tuple is a sequence, so it can be index
    print ("{:.2f}".format(volts) + " CB1 Volts")
    

    amp = ''.join(chr(j) for j in Amps)
    c = struct.unpack('<f', amp)  # '<' for little-endian
    current = c[0] # A tuple is a sequence, so it can be index
    print ("{:.2f}".format(current) + " CB1 Amps")

    #Calculate Power (Watts)
    watts= volts*current
    print ("{:.2f}".format(watts) + " CB1 Watts")
  
  

    with connection.cursor() as cursor:
        sql = "INSERT INTO CB1 (Volts, Current, Watts) VALUES (%s, %s, %s)"
        cursor.execute(sql,(volts, current, watts))
        connection.commit()
        
##    connection.close()

        #execfile("Receive_Arduino_Floats_CB2.py")

   

    
##------------------Store to database-----------------------------##
