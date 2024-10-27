import cv2
import ffmpeg_python

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()
cap = cv2.VideoCapture(0)

width, height = 640, 480

process = (
  ffmpeg
    .input('pipe:', format='rawvideo', pix_fmt='bgr24', s='{}x{}'.format(width, height))
    .output('pipe':, format='rawvideo', pix_fmt='rgb24')
    .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
)
out, err = process.communcate(input=input_data)

def stream():
  global stream
  while True:
    ret, img = cap.read()

@app.get('/')
def main():
  return StreamingResponse(stream(), media_type='video/mp4')
