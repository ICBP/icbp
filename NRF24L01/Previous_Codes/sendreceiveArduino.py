import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev


GPIO.setmode (GPIO.BCM)

#Send and receive addresses

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0XE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

# Setup Radio?
radio = NRF24 (GPIO, spidev.SpiDev())
radio.begin(0,17)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()


radio.openWritingPipe(pipe[0])
radio.openReadingPipe(1, pipe[1])
radio.printDetails()
# radio.startListening()  Since is master no listeing


message = list ("GETSTRING")
while  len(message) <32:
    message.append(0)
    


while True:

    start = time.time()
    radio.write(message)
    print("Sent the message: {}".format(message))
    radio.startListening()

    
    

    while not radio.available(0):
        time.sleep (1/100)
        if time.time() - start > 2:
            print ("Time out.")
            break

        

    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print ("Received: {}".format(receivedMessage))

    print("Translating received Message into unicode charaters...")
    string =""

    for n in receivedMessage:
        if (n >=32 and n< 126):
            string +=chr(n)

    print("Our received message decodes to: {}".format(string))
    

radio.stopListening()
time.sleep(1)
