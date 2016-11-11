import sys
########################Modules Path Information################################
sys.path.append("/usr/lib/pymodules/ICBP_modules")
sys.path.append("/usr/lib/NRF24")
########################Modules Path Information################################
from lib_nrf24 import NRF24
import radio2
import time


while True:
    
    #### Radio.py module configures transceiver information for primary Arduino
    #### located:  /usr/lib/pymodules/ICBP_modules/Radio.py
   # radio.radio_func("radio1")


    
    #### Radio2.py module configures transceiver information for secondary Arduino
    #### located:  /usr/lib/pymodules/ICBP_modules/Radio.py
   # radio.radio_func("radio2")
    

 
    radio2.radio_func("radio3")
