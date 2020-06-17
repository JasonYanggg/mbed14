import pyb
import sensor, image, time, os, tf, math

uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)
tmp = ""
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

def image_classification():
    matrices = 0
    while (not matrices):
       clock.tick()
       img = sensor.snapshot()
       img.lens_corr(1.8) # strength of 1.8 is good for the 2.8mm lens.
       matrices = img.find_qrcodes()
       for code in matrices:
          img.draw_rectangle(code.rect(), color = (255, 0, 0))
          uart.write(code[4].encode())
          uart.write("\r\n".encode())

while(1):
   a = uart.readline()
   if a is not None:
      tmp += a.decode()
      print(a.decode())

   if tmp == "image_classification":
      print("classify images")
      tmp =""
      image_classification()
