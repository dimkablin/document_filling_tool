"""Speech2text Router redirecting"""
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import requests
from src.env import SPEECH2TEXT_URL


router = APIRouter()


@router.get("/get-model-names")
async def get_model_names():
    """Redirects request to get model names."""
    session = requests.Session()
    session.trust_env = False
    response = session.get(f"{SPEECH2TEXT_URL}/get-model-names")
    return JSONResponse(status_code=response.status_code, content=response.json())


@router.get("/get-current-model")
async def get_current_model():
    """Redirects request to get current model."""
    session = requests.Session()
    session.trust_env = False
    response = session.get(f"{SPEECH2TEXT_URL}/get-current-model")
    return JSONResponse(status_code=response.status_code, content=response.json())


@router.post("/predict")
async def predict(audio: UploadFile = File(...)):
    """Redirects request for speech to text."""
    session = requests.Session()
    session.trust_env = False
    files = {'audio': (audio.filename, audio.file)}
    response = session.post(f"{SPEECH2TEXT_URL}/speech-to-text", files=files)
    return JSONResponse(status_code=response.status_code, content=response.json())


@router.get("/get-model-config")
async def get_model_config(model_name: str):
    """Redirects request to get model configuration."""
    session = requests.Session()
    session.trust_env = False
    response = session.get(f"{SPEECH2TEXT_URL}/get-model-config?model_name={model_name}")
    return JSONResponse(status_code=response.status_code, content=response.json())


@router.post("/change-model")
async def change_model(model_name: str, config: dict):
    """Redirects request to change the model."""
    session = requests.Session()
    session.trust_env = False
    response = session.post(f"{SPEECH2TEXT_URL}/change-model?model_name={model_name}", json=config)
    return JSONResponse(status_code=response.status_code, content=response.json())
 