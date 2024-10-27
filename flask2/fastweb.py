from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from v4l2py import Device

app = FastAPI()

def gen_frames():
    with Device.from_id(0) as cam:
        for frame in cam:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame.data + b"\r\n"

@app.get("/")
def index():
    return '<html><img src="/stream" /></html>'

@app.get("/stream")
def stream():
    return StreamingResponse(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
