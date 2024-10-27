from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get('/')
def main():
  return FileResponse('/dev/video0')
  
