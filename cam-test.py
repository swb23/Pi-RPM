#!/usr/bin/python
# -*- coding: utf-8 -*-
import picamera
import datetime as dt

camera = picamera.PiCamera(resolution=(1024, 768), framerate=24)
camera.annotate_background = picamera.Color('black')
camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
a=str(dt.datetime.now()+'.h264')
camera.start_recording(a)
start = dt.datetime.now()
while (dt.datetime.now() - start).seconds < 30:
    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.wait_recording(0.2)
camera.stop_recording()
