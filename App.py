from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os

app = FastAPI()
UPLOAD_DIR = './uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post('/upload-image')
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR,file.filename)
    content = await file.read()
    with open(file_path, 'wb') as f:
        f.write(content)

    return JSONResponse(content={
        'status':'ok',
        'filename': file.filename,
        'message': "Imagen recibida y guardada"
    })