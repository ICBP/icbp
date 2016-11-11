from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
import pymysql.cursors
import spidev
import Unpack
import array
import math
import time

##--------------Collecting Data From Arduino------------------------------##

GPIO.setmode (GPIO.BCM)
GPIO.setwarnings(False)
radio = NRF24 (GPIO, spidev.SpiDev())  # Setup Radio
radio.begin(0,17)
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.startListening()
pipes = [[0xF0, 0xF0, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xD2]]
radio.openReadingPipe(1, pipes[1])
radio.printDetails()


while True:

    while not radio.available():
        time.sleep (2)


    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    #print ("Received from Arduino: {}".format(receivedMessage))

#### unpack_function is a module that translates and stores values into CB1 table
    Unpack.unpack_func(receivedMessage)

    time.sleep(2)
    
          
#################################Second Arduino





    
##------------------Store to database-----------------------------##
