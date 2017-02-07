import numpy as np
import cv2
import time
import picamera



face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_eye.xml')

start = time.time()

roi_face_x = 0
roi_face_y = 0
roi_face_w = 299
roi_face_h = 299   #setting up the initial roi, = entire picture

looplimit = 60
loopcount = 0
while loopcount < looplimit:
  #print '1st roi'
  #print roi_face_x, roi_face_y, roi_face_w, roi_face_h
  img = cv2.imread('/home/pi/img.jpg')
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  roi_face_gray = gray[roi_face_y:(roi_face_y + roi_face_h),roi_face_x:(roi_face_x + roi_face_w)]
  roi_face_color = img[roi_face_y:(roi_face_y + roi_face_h),roi_face_x:(roi_face_x + roi_face_w)]
  #^setting up roi for face
  
  
  faces = face_cascade.detectMultiScale(roi_face_gray, 1.3, 5)
  #print '1st elements in faces'
  #print faces
  cv2.rectangle(img,(roi_face_x, roi_face_y),(roi_face_x + roi_face_w, roi_face_y + roi_face_h),(0,255,0),2) 
  #^draw a box around the area of interest#
  
  #print 'draw a box around the roi' 
  for (x,y,w,h) in faces:
     #print '2nd elements in faces'
     #print x,y,w,h
     cv2.rectangle(roi_face_color,(x,y),(x + w, y + h),(255,0,0),2)
     #print 'draw a box around face(s)'
     
     roi_face_x += x
     roi_face_y += y
     roi_face_w = w
     roi_face_h = h
     #^pass the elements in faces to roi
     #cv2.rectangle(img,(roi_face_x,roi_face_y),(roi_face_x + roi_face_w,roi_face_y + roi_face_h),(255,0,0),2)
     roi_eyes_gray = roi_face_gray[y:(y+(h*2/3)), x:x+w]
     roi_eyes_color = roi_face_color[y:(y+(h*2/3)), x:x+w]
     
     #^only scan upper 2/3 of face for eyes
     eyes = eye_cascade.detectMultiScale(roi_eyes_gray)
     for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_eyes_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        #^draw a box around the eye(s)

  #print '2nd roi,after adjustments'
  #print roi_face_x, roi_face_y, roi_face_w, roi_face_h
  roi_face_x -= 40
  roi_face_y -= 40
  roi_face_w += 80
  roi_face_h += 80
  
  
  loopcount += 1
  #finish = time.time()
        
finish = time.time()
print (faces)
print "time = %d"%(finish - start)
cv2.imshow('img',img)
cv2.waitKey(0)


