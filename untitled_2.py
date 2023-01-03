# Untitled - By: Administrator - 周日 12月 18 2022

import sensor, image, time
import utime
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()
cnt = 0

while(True):
    clock.tick()
    img = sensor.snapshot()
    start = utime.ticks_ms()
    img.save(str(cnt)+".jpg")
    end = utime.ticks_ms()
    print(end-start)
    cnt+=1
    #print(clock.fps())
