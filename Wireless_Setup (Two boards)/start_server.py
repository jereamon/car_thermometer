import network
import socket
import time
import display
ap_if = network.WLAN(network.AP_IF)

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s.bind(addr)

    print("Listening on: ", addr)
    display.display.text("Server", 10, 15)
    display.display.text("Listening", 10, 25)
    display.display.show()
    
    first_run = True
    prior_vals = [-1, -1, -1, -1]

    try:
        while True:
            bytesAddressPair = s.recvfrom(1024)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            
            if first_run:
                display.clear_screen()
                first_run = False
            temps = message.decode().split()
            print("Temps: {}".format(temps))

            img_str = ""
            thirds = False
            if len(temps) > 3:
                if temps[0] == "-":
                    # TODO: implement negative temperature functionality
                    del temps[0]
                    pass
                else:
                    img_str += "thirds-"
                    thirds = True
                
            for i, val in enumerate(temps[:-1]):                
                if thirds:
                    if prior_vals[i] != int(val):
                        display.show_image(img_str + val + '.pbm', i * 37) # y is zero
                        prior_vals[i] = int(val)
                else:
                    prior_vals[0] = -1
                    if prior_vals[i+1] != int(val):
                        print("setting image: {}".format(img_str))
                        display.show_image(img_str + val + '.pbm', x=(i * 55)) # y is zero
                        prior_vals[i+1] = int(val)
                
            if prior_vals[-1] != int(temps[-1]):
                display.show_image("dot" + temps[-1] + ".pbm", 103, 39)
                # ^^ x = 110 and y = 39 because the image is 25x25
                prior_vals[-1] = int(temps[-1])

#             s.sendto("Message received", address)
    except KeyboardInterrupt:
        print("Server interrupted")