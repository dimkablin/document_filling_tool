"""OCR Router redirecting"""
from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
import requests
from src.api.models.data import OCRResultModel
from src.env import OCR_URL


router = APIRouter()


@router.get("/get-model-names", response_model=list)
async def get_model_names() -> list:
    """Return a list of model names."""
    session = requests.Session()
    session.trust_env = False
    response = session.get(f"{OCR_URL}/get-model-names")
    return response.json()


@router.get("/get-current-model", response_model=str)
async def get_current_model() -> str:
    """Return the name of the current model."""
    session = requests.Session()
    session.trust_env = False
    response = session.get(f"{OCR_URL}/get-current-model")
    return response.json()


@router.post("/predict", response_model=OCRResultModel)
async def predict(image: UploadFile) -> OCRResultModel:
    """Predict function."""
    with image.file as file:
        files = {'image': (image.filename, file)}
        session = requests.Session()
        session.trust_env = False
        response = session.post(f"{OCR_URL}/ocr", files=files)
        return response.json()


@router.get("/change-model")
async def change_model(model_name: str):
    """Change the model"""
    session = requests.Session()
    session.trust_env = False
    response = session.get(f"{OCR_URL}/change-model?model_name={model_name}")
    return response.json()
