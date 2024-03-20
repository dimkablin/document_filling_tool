"""Env file"""
import os

project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
DATA_PATH = "./src/data"

IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "webp"}
FILE_EXTENSIONS = {"pdf", "xps", "epub", "mobi", "fb2", "cbz", "txt"}

OCR_URL = os.getenv("OCR_URL", default="http://localhost:8000")
SPEECH2TEXT_URL = os.getenv("SPEECH2TEXT_URL", default="http://localhost:8001")
