import sys
########################Modules Path Information################################
sys.path.append("/home/pi/Desktop/NRF24L01/modules")
########################Modules Path Information################################
import Unpack
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev



def radio_func():
    GPIO.setmode (GPIO.BCM)
    GPIO.setwarnings(False)
    radio1 = NRF24 (GPIO, spidev.SpiDev())
        

    #Send and receive addresses
    pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0XE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xB5]]

    #begin radio and pass CSN to gpio (8/ce0) and CE to gpio 17
    radio1.begin(0,17)

    #Max bytes 32
    radio1.setPayloadSize(32)
    radio1.setChannel(0x76)
    radio1.setDataRate(NRF24.BR_1MBPS)
    radio1.setPALevel(NRF24.PA_MIN)

    radio1.setAutoAck(False)
    radio1.enableDynamicPayloads()
    radio1.enableAckPayload()

    radio1.startListening()
    radio1.openReadingPipe(1, pipes[1])
    #radio1.printDetails()

    while not radio1.available():
        time.sleep (1/1000)

    receivedMessage = []
    radio1.read(receivedMessage, radio1.getDynamicPayloadSize())



    #### unpack_function is a module that translates and stores values into CB1 table
    Unpack.unpack_func(receivedMessage)

    time.sleep(1/1000)

