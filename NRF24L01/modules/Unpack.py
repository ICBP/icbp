import pymysql.cursors
import DBConnect
import struct
import array
import ctypes

def unpack_func(BitStream = []):

    connection = pymysql.connect(host='localhost',
    user='root',
    password='root',
    db='ICBP',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
    
    #radio.read(BitStream, radio.getDynamicPayloadSize())
    #print ("Received from Arduino: {}".format(BitStream))
  
    #print str(BitStream)[1:-1]
    #print ""
    
    
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

    with connection.cursor() as cursor:
        sql = "INSERT INTO CB1 (Volts, Current, Watts) VALUES (%s, %s, %s)"
        cursor.execute(sql,(volts, current, watts))
        connection.commit()


    
    
    
