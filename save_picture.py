# Untitled - By: Administrator - 周三 12月 14 2022

import sensor, image, time
import pyb
import ustruct
bus = pyb.I2C(2, pyb.I2C.SLAVE, addr=0x12)
bus.deinit() # 完全关闭设备
bus = pyb.I2C(2, pyb.I2C.SLAVE, addr=0x12)
print("Waiting for Arduino...")
time.sleep_ms(100)

def i2cRecv():
    data = bytearray(13)
    while(True):
        try:
            try:
                length_data = bus.recv(1)
                d = ustruct.unpack("<%ds" % len(length_data), length_data)[0]
            except OSError as err:
                print(err)
                continue
                pass
            da = bus.recv(int.from_bytes(d, "big"))
            d = ustruct.unpack("<%ds" % len(da), da)
            print(da)
            return da

        except OSError as err:
            print(err)
            pass


BLUE_LED_PIN = 3
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()
cnt = 0



while(True):
    pyb.LED(BLUE_LED_PIN).on()
    clock.tick()
    #img = sensor.snapshot()
    name = i2cRecv()
    path = ".\\picture\\" + str(name) + ".jpg"
    sensor.snapshot().save(path)
    print(clock.fps())
    cnt += 1
    pyb.LED(BLUE_LED_PIN).off()
