""" FastAPI connection """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .endpoints import base, data, ocr, speech2text

app = FastAPI(
    title="Backend API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    openapi_tags=[{
        "name": "Backend API",
        "description": "Backend API router."
    }]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.include_router(base.router, prefix="/api", tags=["base"])
app.include_router(data.router, prefix="/api", tags=["data"])
app.include_router(ocr.router, prefix="/api/ocr", tags=["ocr"])
app.include_router(speech2text.router, prefix="/api/speech2text", tags=["speech2text"])

app.mount("/files", StaticFiles(directory="./src/data"), name="images")
