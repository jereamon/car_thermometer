# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()

import network
ap_if = network.WLAN(network.AP_IF)
ap_if.active(True)
ap_if.config(essid="Thermometer", password="my_thermo")

import start_server
start_server.start_server()

# import display