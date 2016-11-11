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
    radio2 = NRF24 (GPIO, spidev.SpiDev())
        

    #Send and receive addresses
    pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0XE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xC3]]

    #begin radio and pass CSN to gpio (8/ce0) and CE to gpio 17
    radio2.begin(0,17)

    #Max bytes 32
    radio2.setPayloadSize(32)
    radio2.setChannel(0x76)
    radio2.setDataRate(NRF24.BR_1MBPS)
    radio2.setPALevel(NRF24.PA_MIN)

    radio2.setAutoAck(False)
    radio2.enableDynamicPayloads()
    radio2.enableAckPayload()

    radio2.startListening()
    radio2.openReadingPipe(1, pipes[1])
    #radio2.printDetails()

    while not radio2.available():
        time.sleep (1/1000)

    receivedMessage = []
    radio2.read(receivedMessage, radio2.getDynamicPayloadSize())


    #### unpack_function is a module that translates and stores values into CB1 table
    Unpack.unpack_func(receivedMessage)

    time.sleep(1/1000)

