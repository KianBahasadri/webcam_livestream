from fastapi import FastAPI
from fastapi.responses import StreamingResponse, Response, FileResponse
app = FastAPI()

def foo():
  with open('vid.mp4', 'rb') as file:
    b = file.read()
  while True:
    yield b

@app.get('/')
def index():
  return FileResponse('index.html')
@app.get("/vid")#,responses={200:{"content":{"video/mp4":{}}}},response_class=Response)
def get_vid():
    return StreamingResponse(foo(), media_type="video/mp4")

