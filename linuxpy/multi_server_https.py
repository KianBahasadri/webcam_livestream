from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from linuxpy.video.device import Device, VideoCapture
import threading
import time

app = FastAPI()

next_frame = None
frame_condition = threading.Condition()

def capture_frames():
  global next_frame
  dev_source = Device.from_id(0)
  with dev_source:
    source = VideoCapture(dev_source)
    source.set_format(1280, 720, "MJPG")
    with source:
      for frame in source:
        with frame_condition:
          next_frame = (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame.data + b"\r\n")
          frame_condition.notify_all()

capture_thread = threading.Thread(target=capture_frames)
capture_thread.daemon = True
capture_thread.start()

time.sleep(1)

def gen_frames():
  while next_frame is None:
    time.sleep(0.1)
  while True:
    with frame_condition:
      frame_condition.wait()
      yield next_frame

@app.get("/")
def index():
    return FileResponse('index.html')

@app.get("/stream")
def stream():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')



