#Senior Project Driver Fatigue System (main program)

import time
import picamera
import webbrowser
import io
import os
import cv2
import numpy as np
import spidev
import RPi.GPIO as GPIO
#import all libraries needed

#----------prepare FSR sensor---------------------------------------------------
GPIO.setwarnings(False)
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts
  
def ConvertTemp(data,places):
 
  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  465      100    1.50
  #  775      200    2.50
  # 1023      280    3.30
 
  temp = ((data * 330)/float(1023))-50
  temp = round(temp,places)
  return temp

 # Define sensor channels
pressure_channel = 0

 # Define delay between readings
delay = .1

#----------end of FSR preparation-----------------------------------------------

#----------start of face detection part-----------------------------------------

face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_eye.xml')

roi_face_x = 0
roi_face_y = 0
roi_face_w = 299
roi_face_h = 299   #setting up the initial roi = entire picture

runlimit = 60
runcount = 0
eyeindex = 0

with picamera.PiCamera() as camera:
  camera.start_preview()
  time.sleep(3)

while True:
  frames = 5
  deletecount = 0

  def filenames():
    frame = 0
    while frame < frames:
        yield 'image%02d.jpg' % frame
        frame += 1
  with picamera.PiCamera() as camera:
    camera.resolution = (300, 300)
    camera.framerate = 5
    
    start = time.time()
    
    camera.capture_sequence(filenames(),use_video_port=True)
    finish = time.time()
    looplimit = 3
    #^set up how many pics to scan in 1 loop
    loopcount = 0
    while loopcount < looplimit:
      #print loopcount
      img = cv2.imread('/home/pi/image%02d.jpg'%loopcount)
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      roi_face_gray = gray[roi_face_y:(roi_face_y + roi_face_h),roi_face_x:(roi_face_x + roi_face_w)]
      roi_face_color = img[roi_face_y:(roi_face_y + roi_face_h),roi_face_x:(roi_face_x + roi_face_w)]
      #^setting up roi for face
  
  
      faces = face_cascade.detectMultiScale(roi_face_gray, 1.3, 5)
  
      cv2.rectangle(img,(roi_face_x, roi_face_y),(roi_face_x + roi_face_w, roi_face_y + roi_face_h),(0,255,0),2) 
      #^draw a box around the area of interest
      if len(faces) == 0:
         print "no faces where are you"
      for (x,y,w,h) in faces:
     
         #cv2.rectangle(roi_face_color,(x,y),(x + w, y + h),(255,0,0),2)
         #^draw a box around the face
         if x >= 0:
           print 'face detected'
         #time.sleep(3)
         #^wait 3 seconds
         roi_face_x += x
         roi_face_y += y
         roi_face_w = w
         roi_face_h = h
         #^pass the elements in faces to roi
    
         roi_eyes_gray = roi_face_gray[y:(y+(h*50/100)), x:x+w]
         roi_eyes_color = roi_face_color[y:(y+(h*50/100)), x:x+w]  
         #^only scan upper 1/2 of face for eyes
         eyes = eye_cascade.detectMultiScale(roi_eyes_gray)
         for (ex,ey,ew,eh) in eyes:
            #cv2.rectangle(roi_eyes_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            #draw a box around eyes
            if ex >= 0:
              print 'eyes detected'
              eyeindex = 0
         if len(eyes) == 0:
            print 'eyes not detected'
            eyeindex += 1
            print eyeindex
            if eyeindex > 0:
              
              GPIO.setmode(GPIO.BOARD)
              GPIO.setup(16,GPIO.OUT)
              GPIO.output(16,0)
              GPIO.output(16,1)
              time.sleep(.3)
              GPIO.cleanup()

              GPIO.setmode(GPIO.BOARD)
              GPIO.setup(15, GPIO.OUT)
              #^buzzer
              P = GPIO.PWM(15,100)
              P.start(30)
              time.sleep(.3)
              GPIO.cleanup()
              
              
            

  
      roi_face_x -= 50
      if roi_face_x <= 0:
         roi_face_x = 0
      roi_face_y -= 50
      if roi_face_y <= 0:
         roi_face_y = 0
      roi_face_w += 100
      roi_face_h += 100

      loopcount += 1
      
      if (runcount%20 == 0) and (runcount > 1):
        roi_face_x = 0
        roi_face_y = 0
        roi_face_w = 299
        roi_face_h = 299
        print 'roi reset'
        #scan the entire region every 25 frames
      #finish = time.time()
      runcount += 1 
    finish = time.time()
    print (faces)
    print "time = %d"%(finish - start)
    #cv2.imshow('img',img)
    #cv2.waitKey(0)
  while deletecount < frames:
    if os.path.exists("/home/pi/image%02d.jpg"%deletecount):
       os.remove("/home/pi/image%02d.jpg"%deletecount)
       deletecount += 1  #deletes them
  
  #print"%d pictures taken, framerate = %d"%(frames,(frames/(finish-start)))
  #print"runcount = %d"%runcount
  
#----------end of face detection part-----------------------------------------

#----------start of FSR part--------------------------------------------------
  
  # Read the light sensor data
  pressure_level = ReadChannel(pressure_channel)
  pressure_volts = ConvertVolts(pressure_level,2)
  # Print out results
  print ("--------------------------------------------")
  print("Pressure: {} ({}V)".format(pressure_level,pressure_volts))
  while pressure_level < 900:
    print ("HANDS OFF WHEEL!!!!!")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16,GPIO.OUT)
    #^LED
    GPIO.output(16,0)
    GPIO.output(16,1)
    time.sleep(.3)
    GPIO.cleanup()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(15, GPIO.OUT)
    #^buzzer
    P = GPIO.PWM(15,100)
    P.start(30)
    time.sleep(.3)
    GPIO.cleanup()
    pressure_level = ReadChannel(pressure_channel)

##    GPIO.cleanup()
  
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(16,GPIO.OUT)
  GPIO.output(16,0)
  time.sleep(0.1)

# Wait before repeating loop  while True:
  
    
#----------end of FSR part--------------------------------------------------
#----------end--------------------------------------------------------------
