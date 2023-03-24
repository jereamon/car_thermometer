from machine import Pin
import usocket as socket
import network
import utime
import select
import read_temp

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
inner_loop_break = False
led = Pin(2, Pin.OUT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(3)


def flash_led():
    led.off()
    utime.sleep_ms(150)
    led.on()
    utime.sleep_ms(15)
    

def send_temp(temp):
    vals = []
    if temp < 0:
        vals.append("-")
        temp = abs(temp)
        
    if temp == 0 and len(str(temp)) == 1:
        vals = ['0', '0', '0']
    else:
        if temp < 10:
            vals.append('0')
            
        for val in str(temp):
            try:
                int(val) # this ensures the decimal point isn't added to the array.
                # ^^ throws a value error if not a number
                vals.append(val)
            except ValueError:
                pass # val is the period separating the decimal.
        print(vals)
    
    msg = str.encode(" ".join(vals))
    s.sendto(msg, ("192.168.4.1", 80))
            
#     try:
#         msg_from_server = s.recvfrom(1024)
#         print("Message from server: " + str(msg_from_server[0]))
#     except OSError:
#         print("Message receive timeout")


try:
    while True:
        if not sta_if.isconnected():
            print("outer if, sta_if not connected")
            counter = 0
            try:
                print("\nConnecting to wifi")
                print(sta_if.isconnected())
                sta_if.connect("Thermometer", "my_thermo")
                
                counter += 1
                
                while not sta_if.isconnected():
                    if counter > 4:
                        break
                    utime.sleep(1)
                    counter += 1
            except KeyboardInterrupt:
                print("\nInterrupted while connecting to wifi.")
                inner_loop_break = True
        else:
            temps = read_temp.read_temp() # returns tempC and tempF as an array
#             send_temp(temps[1])
            
            test_temps = [-35.2, 110.0, 55.3, 45.4, 33.3]
            for test_temp in test_temps:
                send_temp(test_temp)
                utime.sleep(5)
            

            flash_led()
            flash_led()
            flash_led()
            utime.sleep(2)
            
        if inner_loop_break:
            raise KeyboardInterrupt
except KeyboardInterrupt:
    print("Interrupted in main loop")