from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from linuxpy.video.device import Device, VideoCapture
import threading
import time

app = FastAPI()

next_frame = None

def capture_frames():
  global next_frame
  dev_source = Device.from_id(0)
  with dev_source:
    source = VideoCapture(dev_source)
    source.set_format(1280, 720, "MJPG")
    with source:
      for frame in source:
        next_frame = (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame.data + b"\r\n")

capture_thread = threading.Thread(target=capture_frames)
capture_thread.daemon = True
capture_thread.start()

time.sleep(1)

def gen_frames():
  i = 0
  with open('vid.mpjg', 'wb') as file:
    while next_frame:
      time.sleep(0.01)
      file.write(next_frame)
      i += 1
      if i > 50:
        break


gen_frames()
