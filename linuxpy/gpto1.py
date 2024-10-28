from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from linuxpy.video.device import Device, VideoCapture
import threading

app = FastAPI()

# Global variables to store the latest frame and synchronize access
latest_frame = None
frame_lock = threading.Lock()
frame_condition = threading.Condition()

def capture_frames():
    global latest_frame
    dev_source = Device.from_id(0)
    with dev_source:
        source = VideoCapture(dev_source)
        source.set_format(1280, 720, "MJPG")
        with source:
            for frame in source:
                with frame_condition:
                    latest_frame = frame.data
                    # Notify all waiting clients that a new frame is available
                    frame_condition.notify_all()

# Start the background frame capturing thread
capture_thread = threading.Thread(target=capture_frames)
capture_thread.daemon = True
capture_thread.start()

def gen_frames():
    while True:
        with frame_condition:
            # Wait until a new frame is available
            frame_condition.wait()
            frame = latest_frame
        if frame is not None:
            # Yield the frame to the client
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"

@app.get("/")
def index():
    return FileResponse('index.html')

@app.get("/stream")
def stream():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

