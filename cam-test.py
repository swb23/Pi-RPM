#!/usr/bin/python
# -*- coding: utf-8 -*-
import picamera
import datetime as dt
import time

camera = picamera.PiCamera(resolution=(1024, 768), framerate=24)
camera.annotate_background = picamera.Color('black')
camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

try:
     # Loop until users quits with CTRL-C
    while True:
          camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
          filename=(dt.datetime.now().strftime('%Y%m%d_%H-%M-%S')+ '.h264')
          camera.start_recording(filename)
          start = dt.datetime.now()
          while True:
               camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
               camera.wait_recording(0.2)
except KeyboardInterrupt:
    camera.stop_recording()
    
    
      


