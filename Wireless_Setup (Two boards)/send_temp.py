import network
import time
import usocket
import socket

sta_if = network.WLAN(network.STA_IF)


def do_connect():
    counter = 0

    print("Trying to connect", end="")
    while not sta_if.isconnected() and counter < 10:
        sta_if.connect('Thermometer', 'my_thermo')
        print(".", end="")
    #     counter += 1
        time.sleep(2)
    
    print()    
    print("Connected to network!")
    sta_if.ifconfig(('192.168.4.3', '255.255.255.0', '192.168.4.1', '192.168.4.1'))
    print("IP addr: " + str(sta_if.ifconfig()))


def send_temp():
    counter = 0
    text = "Counter: "
    
    while True:
        if sta_if.isconnected():
#             try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("192.168.4.1", 80))
            s.send(text + str(counter))
            
            data = s.recv(1024).decode("utf-8")
            print("Data received: " + data) 
            s.close()
            
            counter += 1
            time.sleep(3) # sleep for 3 seconds
#             except OSError as e:
#                 s.close()
#                 do_connect()
        else:
            print("Lost connection")
            do_connect()