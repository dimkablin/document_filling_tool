"""Endpoints for getting version information."""
from typing import List
from fastapi import APIRouter
from fastapi.responses import FileResponse
from ..crud.data import Data

router = APIRouter()


@router.post("/create-excel-from-json")
def create_excel_from_json(json_data: List[List[dict]]):
    """Return a excel file"""
    file_path = Data.create_excel_from_json(json_data)
    return FileResponse(file_path, filename='output.xlsx')
