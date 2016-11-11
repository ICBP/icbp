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
    #### Radio.py module configures transceiver information for primary Arduino
    #### located:  /usr/lib/pymodules/ICBP_modules/Radio.py
    Radio.radio_func()

    #### Radio2.py module configures transceiver information for secondary Arduino
    #### located:  /usr/lib/pymodules/ICBP_modules/Radio.py
    Radio2.radio_func()

 
