import sys
########################Modules Path Information################################
sys.path.append("/usr/lib/pymodules/ICBP_modules")
sys.path.append("/usr/lib/NRF24")
########################Modules Path Information################################
from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
import pymysql.cursors
import spidev
import Unpack
import Unpack2
import array
import math
import time


##--------------Collecting Data From Arduino------------------------------##


while True:

    GPIO.setmode (GPIO.BCM)
    GPIO.setwarnings(False)
    radio2 = NRF24 (GPIO, spidev.SpiDev())  # Setup Radio
    radio2.begin(0,17)
    radio2.setPayloadSize(32)
    radio2.setChannel(0x76)
    radio2.setDataRate(NRF24.BR_1MBPS)
    radio2.setPALevel(NRF24.PA_MIN)
    radio2.setAutoAck(True)
    radio2.enableDynamicPayloads()
    radio2.enableAckPayload()

    radio2.startListening()
    pipes = [[0xF0, 0xF0, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xC3]]
    radio2.openReadingPipe(1, pipes[1])
    #radio2.printDetails()

    
    while not radio2.available():
        time.sleep (1/1000)


    receivedMessage = []
    radio2.read(receivedMessage, radio2.getDynamicPayloadSize())
    #print ("Received from Arduino: {}".format(receivedMessage))

#### unpack_function is a module that translates and stores values into CB1 table
    Unpack.unpack_func(receivedMessage)

    time.sleep(1/1000)


    #while True:


    #################################Second Arduino

    GPIO.setmode (GPIO.BCM)
    GPIO.setwarnings(False)
    radio1 = NRF24 (GPIO, spidev.SpiDev())  # Setup Radio
    radio1.begin(0,17)
    radio1.setPayloadSize(32)
    radio1.setChannel(0x76)
    radio1.setDataRate(NRF24.BR_1MBPS)
    radio1.setPALevel(NRF24.PA_MIN)
    radio1.setAutoAck(True)
    radio1.enableDynamicPayloads()
    radio1.enableAckPayload()

    radio2.startListening()
    pipes = [[0xF0, 0xF0, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xB5]]
    radio1.openReadingPipe(1, pipes[1])
    #radio1.printDetails()
    

    while not radio1.available():
        time.sleep (1/1000)
        

    receivedMessage = []
    radio1.read(receivedMessage, radio1.getDynamicPayloadSize())
    #print ("Received from Arduino: {}".format(receivedMessage))

#### unpack_function is a module that translates and stores values into CB1 table
    Unpack2.unpack_func(receivedMessage)

    time.sleep(1/1000)



    
##------------------Store to database-----------------------------##
