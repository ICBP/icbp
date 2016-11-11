import sys
########################Modules Path Information################################
sys.path.append("/home/pi/Desktop/NRF24L01/modules")
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

