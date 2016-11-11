import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev


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
radio.printDetails()
radio.startListening()

while True:

    while not radio.available(0):
        time.sleep (1/100)

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print ("Received: {}".format(receivedMessage))

    print("Translating received Message into unicode charaters...")
    string =""

    for n in receivedMessage:
        if (n >=32 and n< 126):
            string +=chr(n)

    print("Our received message decodes to: {}".format(string))
    
