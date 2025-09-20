from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os

app = FastAPI()
UPLOAD_DIR = './uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="tAGWVoOgMbywsoht0OBG"
)

@app.post('/upload-image')
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR,file.filename)
    content = await file.read()
    with open(file_path, 'wb') as f:
        f.write(content)

    result = CLIENT.infer(file_path, model_id="recyclable-items/3")
    predictions = result.get("predictions", [])

    clases_detectadas = [pred["class"] for pred in predictions]

    return JSONResponse(content={
        'status': 'ok',
        'filename': file.filename,
        'message': "Imagen recibida y clasificada",
        'clases_detectadas': clases_detectadas
    })
