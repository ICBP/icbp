import pymysql.cursors
import struct
import array
import ctypes
import mySql2
import time


def unpack_func(BitStream = [], rID= ""):

    #BitStream = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    print "Staring Unpack Module"
    print "Unpack receive radio ID =" + rID
    
    #rID.read(BitStream, radio.getDynamicPayloadSize())
    #print ("Received from Arduino: {}".format(BitStream))
  
    print str(BitStream)[1:-1]
    print ""
    
    
    #Break into two set of 4 bytes
    Volts = (BitStream)[0:+4]
    Amps = (BitStream)[4:+8]
    #print Volts #Print the four bytes that represent voltage value
    #print Amps # Print the four bytes that represent current value
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

    time.sleep(100/1000)

    if (watts >0.0):
        status = "1"
        print status
    if (watts == 0.0):
        status = "0"
        print status



    #print "Radio ID passing to Mysql" + rID
    #print ""
    mySql2.mysql_func(rID, volts, current, watts, status) 





    
    
    
