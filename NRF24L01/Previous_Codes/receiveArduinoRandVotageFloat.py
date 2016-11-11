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
### connect to the database you created with the credentials you set up
##connection = pymysql.connect(host='localhost',
##    user='root',
##    password='root',
##    db='ICBP',
##    charset='utf8mb4',
##    cursorclass=pymysql.cursors.DictCursor)
### END CODE


##--------------Collecting Data From Arduino------------------------------##

GPIO.setmode (GPIO.BCM)

#Send and receive addresses
pipe = [[0xE8, 0xE8, 0xF0, 0xF0, 0XE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

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
        time.sleep (3)

## Print array
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print ("Received: {}".format(receivedMessage))

    #print str(receivedMessage)[1:-1]
    data = (receivedMessage)[0:+4]
    print data
    
    b = ''.join(chr(i) for i in data)
    print struct.unpack('<f', b)
   
    


    
    

    
##    string =""
##
##    for n in receivedMessage:
##        if (n >=32 and n< 126):
##            string +=chr(n)
##
##    print("Our received message decodes to: {}".format(string))


    


####Store values into variables
##    volts= receivedMessage[0]
##    print ("{:.2f}".format(volts) + " Volts")

   

##    current= receivedMessage[2]
##    print ("{:.2f}".format(current) + " Amps")
##
####Calculate Power (Watts)
##    watts= volts*current
##    print ("{:.2f}".format(watts) + " Watts")
##    w=watts



##    with connection.cursor() as cursor:
##        sql = "INSERT INTO CB1 (Volts, Current, Watts) VALUES (%s, %s, %s)"
##        cursor.execute(sql,(volts, current, watts))
##        connection.commit()
####    connection.close()

   

    
##------------------Store to database-----------------------------##
