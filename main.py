#!/home/kian/opencv/venv/bin/python3
import cv2 as cv
from threading import Thread
import av
import io

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

# init cap
cap = cv.VideoCapture(0)
if not cap.isOpened():
  print("Cannot open Camera")
  exit(1)

width, height, fps = 192, 108, 24  # Select video resolution and framerate.
buffer = io.BytesIO()
output = av.open(buffer, 'w', format="mp4")
stream = output.add_stream('h264', rate=fps)
stream.width = width
stream.height = height
stream.pix_fmt = 'yuv444p'
stream.options = {'crf': '17'}

packet = None

def get_frame():
  global packet
  while True:
    ret, frame = cap.read()
    if not ret:
      print("Can't receive frame (stream end?). Exiting ...")
      exit(1)
    #cv.imshow('frame', frame)
    cv.waitKey(1)
    frame_av = av.VideoFrame.from_ndarray(frame)#, format='bgr24')
    packets = stream.encode(frame_av)
    packet = packets[0]

t1 = Thread(target=get_frame)
t1.start()
breakpoint()

async def video_streamer():
      yield packet.to_bytes()

@app.get('/video.mp4')
async def main():
  return StreamingResponse(video_streamer())

