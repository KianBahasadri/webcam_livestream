import imageio as iio
import time

def gen():
  camera = iio.get_reader("<video0>")
  meta = camera.get_meta_data()
  num_frames = 3 * int(meta["fps"])
  delay = 1/meta["fps"]

  buffer = list()
  for frame_counter in range(num_frames):
      frame = camera.get_next_data()
      buffer.append(frame)
      time.sleep(delay)

  camera.close()

  import io
  memory = io.BytesIO()
  iio.mimwrite(memory, buffer, 'mp4', macro_block_size=8, fps=meta["fps"])

  yield memory.getvalue()

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, Response
app = FastAPI()
@app.get("/",responses={200:{"content":{"video/mp4":{}}}},response_class=Response)
def get_vid():
    return StreamingResponse(gen(), media_type="video/mp4")

