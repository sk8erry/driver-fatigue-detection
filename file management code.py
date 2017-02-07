import time
import picamera
import webbrowser
import io
import os
import numpy as np

runlimit = 1000
runcount = 0
with picamera.PiCamera() as camera:
  camera.start_preview()
  time.sleep(3)

while runcount < runlimit:
  frames = 13
  deletecount = 0

  def filenames():
    frame = 0
    while frame < frames:
        yield 'image%02d.jpg' % frame
        frame += 1
  with picamera.PiCamera() as camera:
    camera.resolution = (300, 300)
    camera.framerate = 15
    
    start = time.time()
    
    camera.capture_sequence(filenames(),use_video_port=True)
    finish = time.time() #takes 60 pics

  while deletecount < frames:
    if os.path.exists("/home/pi/image%02d.jpg"%deletecount):
       os.remove("/home/pi/image%02d.jpg"%deletecount)
       deletecount += 1  #deletes them
  runcount += 1
  print"%d pictures taken, framerate = %d"%(frames,(frames/(finish-start)))
  print"loop count = %d"%runcount
  
