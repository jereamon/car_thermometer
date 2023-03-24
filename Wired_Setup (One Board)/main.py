from utime import sleep, sleep_ms
from os import urandom
import display
import read_temp

prior_vals = ['-1', '-1', '-1', '-1']

def random_float(upper=10, lower=0):
    raw_int = int.from_bytes(urandom(5), "big")
    floater = round(((raw_int % 1000) / 1000) * (upper-lower) + lower, 1)
    
    return floater


def parse_temp(temp):
    '''
    Takes a string temperature representing a float temperature value
    such as: "32.4".
    '''
    temp = str(temp) # just in case I accidentally pass a float in
    
    global prior_vals
    img_str = ""
    thirds = False
    parsed_temp = ""
    
    # -------------------------------------------------------------
    # Checks if the number is negative
    if temp[0] == "-":
        # TODO: implement negative temperature functionality
#         temp = temp[1:]
        parsed_temp += "-"
        pass
    # -------------------------------------------------------------
    
    
    if abs(float(temp)) < 10:
        if len(temp) == 1 and temp == "0":
            parsed_temp += '0'
        parsed_temp += '0'
    
    
    # -------------------------------------------------------------
    # Removes the decimal point so we only have integers to deal with
    for val in temp:
        try:
            int(val)
            parsed_temp += val
        except:
            # removes the decimal point
            pass
    temp = parsed_temp
    # -------------------------------------------------------------

    
    # This means we have three digits before the decimal point
    if len(temp) > 3:
        img_str += "thirds-"
        thirds = True
            
    # -------------------------------------------------------------
    # We now have a string of only integers where the last digit
    # comes after the decimal point and the rest before it.
    # So we check if there are two or three values before the
    # decimal and display the images associated with each value.
    # If the new value is the same as the previous one (stored in prior_vals)
    # we don't bother updating that value.
    reload_dot = False
    for i, val in enumerate(temp[:-1]):
        if thirds:
            if i == 0 and prior_vals[i] == -1: # Going from 2 digits to 3 before the decimal needs screen clear
                    display.clear_screen()
                    prior_vals = ['-1' for _ in range(4)]
                  
            if prior_vals[i] != val:
                if i == 2:
                    reload_dot = True
                    
#                 print(f"showing image: {img_str + val + '.pbm'}")
                display.show_image(img_str + val + '.pbm', i * 36) # y is zero
                prior_vals[i] = val
                prior_vals[i+1] = '-1'
        else:
            if i == 0 and prior_vals[0] != -1: # Going from 3 digits to 2 before the decimal needs screen clear
                    display.clear_screen()
                    prior_vals = ['-1' for _ in range(4)]
                    
            if prior_vals[i+1] != val:
                if i == 2:
                    reload_dot = True
                
#                 print(f"showing image: {img_str + val + '.pbm'}")
                display.show_image(img_str + val + '.pbm', i * 55) # y is zero
                prior_vals[i+1] = val
                prior_vals[i+2] = '-1'
                
            prior_vals[0] = '-1'

    if prior_vals[-1] != int(temp[-1] or reload_dot):
#         print(f"showing image: {"dot" + temp[-1] + ".pbm"}")
        display.show_image("dot" + temp[-1] + ".pbm", 103, 39)
        # ^^ x = 110 and y = 39 because the image is 25x25
        prior_vals[-1] = int(temp[-1])
        
        reload_dot = False
    # -------------------------------------------------------------

def get_and_display_temp():
    try:
        while True:
#             test_temps = ['0', '32.2', '110.2', '-32.5']
#             for temp in test_temps:
#                 print(temp)
#                 parse_temp(str(temp))
#                 sleep(2)
            floater = random_float(150, -50)
            print(floater)
            parse_temp(str(floater))
            sleep(5)
                
#             temps = read_temp.read_temp()
#             print(f"Got temps: {temps}")
#             parse_temp(str(temps[1]))
#             sleep(5)
    except KeyboardInterrupt:
        print("Loop interrupted")


get_and_display_temp()