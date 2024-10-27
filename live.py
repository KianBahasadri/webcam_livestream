import numpy as np
import cv2
import av
import io

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

n_frames = 100
output_memory_file = io.BytesIO()

output = av.open(output_memory_file, 'w', format="mp4")
STREAM = output.add_stream('h264', 30)

cap = cv2.VideoCapture(0)

from threading import Thread
def foo():
  for _ in range(n_frames):
      ret, img = cap.read()

      frame = av.VideoFrame.from_ndarray(img, format='bgr24')
      packets = STREAM.encode(frame)
      output.mux(packets)

t1 = Thread(target=foo)
t1.start()
t1.join()
packets = STREAM.encode(None)
output.mux(packets)
output.close()


app = FastAPI()

def stream():
  print(len(output_memory_file.getvalue()))
  yield output_memory_file.getbuffer().tobytes()

@app.get('/')
def main():
  return StreamingResponse(stream(), media_type='video/mp4')
