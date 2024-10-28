from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from linuxpy.video.device import Device, VideoCapture

app = FastAPI()

def gen_frames():
  dev_source = Device.from_id(0)
  with dev_source:
    source = VideoCapture(dev_source)
    source.set_format(1280, 720, "MJPG")
    with source:
      for frame in source:
          yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame.data + b"\r\n"

@app.get("/")
def index():
    return FileResponse('index.html')

@app.get("/stream")
def stream():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')
