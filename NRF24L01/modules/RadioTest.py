import sys
########################Modules Path Information################################
sys.path.append("/usr/lib/pymodules/ICBP_modules")
sys.path.append("/usr/lib/NRF24")
########################Modules Path Information################################
import UnpackTest
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev


def radio_func(str = ""):
    rID = str
    print "Starting"
    print "Radio ID = " + rID
    
    GPIO.setmode (GPIO.BCM)
    GPIO.setwarnings(False)
    str = NRF24 (GPIO, spidev.SpiDev())

    start = time.time()
    #Send and receive addresses
    pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0XE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xB5]]

 
    #begin radio and pass CSN to gpio (8/ce0) and CE to gpio 17
    str.begin(0,17)

    #Max bytes 32
    str.setPayloadSize(32)
    str.setChannel(0x76)
    str.setDataRate(NRF24.BR_1MBPS)
    str.setPALevel(NRF24.PA_MIN)

    str.setAutoAck(False)
    str.enableDynamicPayloads()
    str.enableAckPayload()

    str.startListening()
    str.openReadingPipe(1, pipes[1])
    #str.printDetails()
    

    while not str.available():
        time.sleep (1/1000)
        
    receivedMessage = []
    str.read(receivedMessage, str.getDynamicPayloadSize())
    
    #### unpack_function is a module that translates and stores values into CB1 table
    #### located:  /usr/lib/pymodules/ICBP_modules/Unpack.py
    print "Radio ID passing to Unpack = " + rID
    print ""
    UnpackTest.unpack_func(receivedMessage, rID)


    time.sleep(100/1000)

