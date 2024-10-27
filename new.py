import numpy as np
import cv2

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

cap = cv2.VideoCapture(0)
def record():
  while True:
      ret, frame = cap.read()
      img = cv2.imencode('.jpg', frame)
      yield img.tobytes()
      

app = FastAPI()

@app.get('/')
def main():
  return StreamingResponse(record())
