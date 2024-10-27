import asyncio
import imageio as iio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

async def gen():
    camera = iio.get_reader("<video0>")
    try:
        meta = camera.get_meta_data()
        num_frames = 3 * int(meta["fps"])
        delay = 1 / meta["fps"]

        for _ in range(num_frames):
            frame = camera.get_next_data()
            # Encode the single frame into bytes
            memory = iio.imwrite('<bytes>', frame, format='jpeg')
            # Yield the frame bytes
            yield memory
            await asyncio.sleep(delay)
    finally:
        camera.close()

app = FastAPI()

@app.get("/")
async def get_vid():
    return StreamingResponse(gen(), media_type="multipart/x-mixed-replace; boundary=frame")

