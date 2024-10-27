import cv2
import ffmpeg
import numpy as np
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

width, height = 640, 480

def stream():
    cap = cv2.VideoCapture(0)
    # Ensure the camera has opened successfully
    if not cap.isOpened():
        raise RuntimeError("Could not start camera.")

    # Open ffmpeg process for frame processing
    process = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt='bgr24', s=f'{width}x{height}')
        .filter('hue', s=0)  # Example filter: desaturate image
        .output('pipe:', format='rawvideo', pix_fmt='bgr24')
        .run_async(pipe_stdin=True, pipe_stdout=True)
    )
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Resize frame if necessary
            frame = cv2.resize(frame, (width, height))
            # Write raw frame to ffmpeg stdin
            process.stdin.write(frame.tobytes())
            # Read processed frame from ffmpeg stdout
            in_bytes = process.stdout.read(width * height * 3)
            if not in_bytes:
                break
            processed_frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])
            # Encode processed frame as JPEG
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            if not ret:
                continue
            frame = buffer.tobytes()
            # Yield frame in HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        cap.release()
        process.stdin.close()
        process.stdout.close()
        process.wait()

@app.get('/')
def main():
    return StreamingResponse(stream(), media_type='multipart/x-mixed-replace; boundary=frame')

