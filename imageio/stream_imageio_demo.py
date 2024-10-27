import imageio as iio
import time

def gen():
  seconds = 1
  camera = iio.get_reader("<video0>")
  meta = camera.get_meta_data()
  num_frames = seconds * int(meta["fps"])
  delay = 1/meta["fps"]

  buffer = list()
  for frame_counter in range(num_frames):
    frame = camera.get_next_data()
    buffer.append(frame)
    time.sleep(delay)
    #yield f"number: {frame_counter} \n".encode()
  memory = iio.mimwrite('<bytes>', buffer, 'mp4', macro_block_size=8, fps=meta["fps"])
  return memory
  camera.close()

def foo():
  for i in range(10):
    yield gen()

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, Response
app = FastAPI()
@app.get("/")#,responses={200:{"content":{"video/mp4":{}}}},response_class=Response)
def get_vid():
    return StreamingResponse(foo())#, media_type="video/mp4")

