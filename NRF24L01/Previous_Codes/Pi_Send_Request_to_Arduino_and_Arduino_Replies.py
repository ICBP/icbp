import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode (GPIO.BCM)

#Send and receive addresses
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0XE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

# Setup Radio
radio = NRF24 (GPIO, spidev.SpiDev())
radio.begin(0,17)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

#OpenwritingPipe to send data out from the Pi to Arduino
radio.openWritingPipe(pipes[0]) #The first address on the Pipe will be use
radio.openReadingPipe(1, pipes[1]) # The second address on the pipe will be use for reading
radio.printDetails()
# radio.startListening()  Since the RPi is the master is not going to startout by listening


#Start executing command example

message = list ("CBI")
#Append zero to send 32 bytes
while  len(message) <32:
    message.append(0)
    


#Time out process
while True:

    start = time.time()
    radio.write(message)
    print("Sent the message: {}".format(message))
    radio.startListening() #Now start listening for a reply from the arduino

    
    #wait until something shows up on the radio    
    while not radio.available(0):
        time.sleep (1/100)
        if time.time() - start > 2:  #Check to carryout the rest of the code
            print ("Time out.")
            break

    ## Print array
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print ("Received: {}".format(receivedMessage))


##Store values into variables
    volts= receivedMessage[0]
    print ("{}".format(volts) + " Volts")

    current= receivedMessage[2]
    print ("{}".format(current) + " Amps")

##Calculate Power (Watts)
    watts= volts*current
    print ("{}".format(watts) + " Watts")
    w=watts

    
    radio.stopListening()
    time.sleep(1)  
