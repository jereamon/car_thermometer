import machine, onewire, ds18x20, time

ds_pin = machine.Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))


# try:
#     while True:
#       ds_sensor.convert_temp()
#       time.sleep_ms(750)
#       for rom in roms:
#         print(rom)
#         print(ds_sensor.read_temp(rom))
#       time.sleep(5)
# except KeyboardInterrupt:
#     print("Interrupted reading temperature")

def read_temp():
    try:
        roms = ds_sensor.scan()
        ds_sensor.convert_temp()
        time.sleep_ms(50)
        tempC = ds_sensor.read_temp(roms[0])
        
        try:
            tempF = (tempC * (9/5)) + 32
            tempC = round(tempC, 1)
            tempF = round(tempF, 1)
        except TypeError: # This means it couldn't read tempC
            tempC = 0
            tempF = 0
            
        return [tempC, tempF]
    except:
        print("Error detecting temperature sensor")
#     for rom in roms:
#         print(ds_sensor.read_temp(rom))