import numpy as np
import cv2
import av
import io

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

n_frmaes = 100  # Select number of frames (for testing).
width, height, fps = 192, 108, 23  # Select video resolution and framerate.

output_memory_file = io.BytesIO()  # Create BytesIO "in memory file".

output = av.open(output_memory_file, 'w', format="mp4")  # Open "in memory file" as MP4 video output
stream = output.add_stream('h264', fps)  # Add H.264 video stream to the MP4 container, with framerate = fps.
stream.width = width  # Set frame width
stream.height = height  # Set frame height
stream.pix_fmt = 'yuv444p'   # Select yuv444p pixel format (better quality than default yuv420p).
stream.options = {'crf': '17'}  # Select low crf for high quality (the price is larger file size).


def make_sample_image(i):
    """ Build synthetic "raw BGR" image for testing """
    p = width//60
    img = np.full((height, width, 3), 60, np.uint8)
    cv2.putText(img, str(i+1), (width//2-p*10*len(str(i+1)), height//2+p*10), cv2.FONT_HERSHEY_DUPLEX, p, (255, 30, 30), p*2)  # Blue number
    return img


# Iterate the created images, encode and write to MP4 memory file.
cap = cv2.VideoCapture(0)
for i in range(n_frmaes):
    ret, img = cap.read()
    #img = make_sample_image(i)  # Create OpenCV image for testing (resolution 192x108, pixel format BGR).
    frame = av.VideoFrame.from_ndarray(img, format='bgr24')  # Convert image from NumPy Array to frame.
    packet = stream.encode(frame)  # Encode video frame
    output.mux(packet)  # "Mux" the encoded frame (add the encoded frame to MP4 file).

# Flush the encoder
packet = stream.encode(None)
output.mux(packet)

output.close()

# Write BytesIO from RAM to file, for testing
with open("output.mp4", "wb") as f:
    f.write(output_memory_file.getbuffer())

#breakpoint()

app = FastAPI()

def stream():
  yield output_memory_file.getbuffer().tobytes()

@app.get('/')
def main():
  return StreamingResponse(stream(), media_type='video/mp4')
