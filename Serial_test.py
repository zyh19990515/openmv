# Untitled - By: Administrator - 周一 10月 17 2022

import sensor, image, time
from pyb import UART
from pyb import USB_VCP

usb = USB_VCP()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
uart = UART(1,9600)
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    usb.send(str(105))
    print(clock.fps())
