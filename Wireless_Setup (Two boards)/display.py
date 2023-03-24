from machine import Pin, I2C
import ssd1306
import framebuf
from utime import sleep, sleep_ms, ticks_ms

i2c = I2C(sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


def clear_screen():
    display.fill(0)
    display.show()


def home_screen(text="Placeholder"):
    display.fill(0)
    display.text(text, 5, 8, 1)
    display.show()


def show_image(image, x=0, y=0):
    try:
        with open("Images/" + image, "rb") as f:
            f.readline()
            f.readline()
            dimensions = [int(val) for val in f.readline().decode().split()]
            
            display.fill_rect(x, y, x + dimensions[0], y + dimensions[1], 0)
            
            data = bytearray(f.read())
            
            fbuf = framebuf.FrameBuffer(data, dimensions[0], dimensions[1], framebuf.MONO_HLSB)
            display.blit(fbuf, x, y)
            display.show()
    except Exception as e:
        print("Error setting image: {}".format(e))