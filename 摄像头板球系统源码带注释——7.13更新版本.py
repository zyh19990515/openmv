import sensor, image, time,pyb   #导入必要的模块
from pyb import UART             #串口
from pyb import LED
Blank=0
k=0
s=0
color=100
the_min=0
green_threshold   = (10,90)   #小球灰度的范围
#具体范围可以连接图像再画一个框，从右下角可以看到范围
uart = UART(3,115200,timeout_char = 1000000)      #初始化串口 波特率115200和控制器通信
ROI=(75,03 ,200,200)         # 窗口大小设置为平板大小和坐标
ROI_2=(00,00,225,215)       #检测动态阈值数据的窗口大小
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE) #灰度模式
sensor.set_framesize(sensor.QVGA)  #选择视觉窗口
sensor.set_windowing(ROI)      #开窗
sensor.skip_frames(10)    #跳过帧
sensor.set_auto_gain(True) #自动增益
sensor.set_auto_whitebal(False) #关闭白平衡
clock = time.clock()
ir_led    = LED(4)#点亮补光灯
while(True):
        clock.tick()
        Blank=0 #Blank=0说明有球，=1说明找不到球
        img = sensor.snapshot()#抓取图像
        if(k<22):
            green_threshold=(10,110) #初始的颜色阈值
        else:
            green_threshold=(10,color) #进入动态阈值模式
        blobs = img.find_blobs([green_threshold],x_stride=10,y_stride=10,area_threshold=20)#找点
        if blobs:       #找到了小球
                for b in blobs:
                    img.draw_cross(b[5],b[6])       #在右上方的监视器画十字叉丝 有多少画多少
        else:
            Blank=1
        if( Blank==1 or the_min>50): #>50这个判断用于检测小球是否真的存在视野中
            output_str=bytearray([0xff,0xfe,0xfd,0xfd])  #打印坐标
        else:
            output_str=bytearray([0xff,0xfe,int(b[5]),int(b[6])])  #打印坐标

        uart.write(output_str)#发送小球坐标

        if(s>20): #每20次更新一次动态阈值
            s=0
            statistics=img.get_statistics(roi=ROI_2)
            color_1=statistics.lq()#获取灰度四分之一数
            color_2=statistics.min()#获取灰度最小值
            color_average=int((color_1+color_2)/2)
            the_min=color_2
            if(color_average>100): #如果大于100说明小球不在视线中
                color_average=100
            color=color_average#动态阈值传递给全局变量

        s=s+1
        ir_led.on()
        #print(the_min)
        if(k<23):
            k=k+1

