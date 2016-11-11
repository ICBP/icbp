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
pipe = [[0xE8, 0xE8, 0xF0, 0xF0, 0XE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xB5], [0xF0, 0xF0, 0xF0, 0xF0, 0xC3]]

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

radio.startListening()
radio.openReadingPipe(1, pipe[1])
radio.openReadingPipe(1, pipe[2])
##radio.printDetails()


while True:

    while not radio.available():
        time.sleep (2)

## Print array
    receivedMessage = [2]
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
    print ("{:.2f}".format(volts) + " Volts")
    

    amp = ''.join(chr(j) for j in Amps)
    c = struct.unpack('<f', amp)  # '<' for little-endian
    current = c[0] # A tuple is a sequence, so it can be index
    print ("{:.2f}".format(current) + " Amps")

    #Calculate Power (Watts)
    watts= volts*current
    print ("{:.2f}".format(watts) + " Watts")
  
  

    with connection.cursor() as cursor:
        sql = "INSERT INTO CB1 (Volts, Current, Watts) VALUES (%s, %s, %s)"
        cursor.execute(sql,(volts, current, watts))
        connection.commit()
       # connection.close()

        time.sleep(2)
                
#################################Second Arduino



## Print array
receivedMessage = [1]
radio.read(receivedMessage, radio.getDynamicPayloadSize())
print ("Received from Arduino: {}".format(receivedMessage))

print str(receivedMessage)[1:-1]
print ""


#Break into two set of 4 bytes
Volts1 = (receivedMessage)[0:+4]
Amps1 = (receivedMessage)[4:+8]
print Volts1 #Print the four bytes that represent voltage value
print Amps1 # Print the four bytes that represent current value
print ""

#The join line converts each integer value into a character byte
#then joins them together into a single string which is what
#the struct.unpack requires as an input

volt1 = ''.join(chr(i) for i in Volts1)
v1 = struct.unpack('<f', volt1)  # '<' for little-endian
volts1 = v1[0] # A tuple is a sequence, so it can be index
print ("{:.2f}".format(volts1) + " Volts")


amp1 = ''.join(chr(j) for j in Amps1)
c1 = struct.unpack('<f', amp1)  # '<' for little-endian
current1 = c1[0] # A tuple is a sequence, so it can be index
print ("{:.2f}".format(current1) + " Amps")

#Calculate Power (Watts)
watts1= volts1*current1
print ("{:.2f}".format(watts1) + " Watts")



with connection.cursor() as cursor:
    sql = "INSERT INTO CB2 (Volts, Current, Watts) VALUES (%s, %s, %s)"
    cursor.execute(sql,(volts1, current1, watts1))
    connection.commit()


time.sleep(2)

    
##------------------Store to database-----------------------------##
