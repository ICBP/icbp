import sys
########################Modules Path Information################################
sys.path.append("/usr/lib/pymodules/ICBP_modules")
sys.path.append("/usr/lib/NRF24")
########################Modules Path Information################################
from lib_nrf24 import NRF24
import Radio
import Radio2
import time


while True:
    start = time.time()
    #### Radio.py module configures transceiver information for primary Arduino
    #### located:  /usr/lib/pymodules/ICBP_modules/Radio.py
    Radio.radio_func()

    if time.time() - start > 2:#Check to carryout the rest of the code
        print ("Time out.")
        break
    
    #### Radio2.py module configures transceiver information for secondary Arduino
    #### located:  /usr/lib/pymodules/ICBP_modules/Radio.py
    Radio2.radio_func()
    
    if time.time() - start > 2:#Check to carryout the rest of the code
        print ("Time out.")
        break
    

 
