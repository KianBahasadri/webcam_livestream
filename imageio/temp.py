import imageio as iio
import matplotlib.pyplot as plt
import time

camera = iio.get_reader("<video0>")
meta = camera.get_meta_data()
num_frames = 2 * int(meta["fps"])
delay = 1/meta["fps"]

def gen_vid_bytes():
  buffer = list()
  for frame_counter in range(num_frames):
      frame = camera.get_next_data()
      buffer.append(frame)
      time.sleep(delay)

  import io
  memory = io.BytesIO()
  iio.mimwrite(memory, buffer, 'mp4', macro_block_size=8, fps=meta["fps"])


  yield memory.getvalue()

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, Response
app = FastAPI()
@app.get("/", responses = { 200: { "content": { "video/mp4": {}}}},response_class=Response)
def get_vid():
    return StreamingResponse(gen_vid_bytes(), media_type="video/mp4")

