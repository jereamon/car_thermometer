import machine, onewire, ds18x20, time

ds_pin = machine.Pin(2)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

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
        return [0,0]
        print("Error detecting temperature sensor")