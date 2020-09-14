# FastAPI modules
from fastapi import APIRouter, HTTPException, File, UploadFile 
import urllib.request

# For listing files
import glob

# Dependencies for saving uploaded file
import shutil
from pathlib import Path

router = APIRouter()

def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

@router.get("/scripts", tags=["pb_pyscripts"])
def scripts_catalog():
    return str(glob.glob("/app/python_scripts/*.py"))

@router.get("/scripts/{script_name}", tags=["pb_pyscripts"])
def obtain_scripts(script_name: str):
    try:
        fopen = open("/app/python_scripts/"+script_name, 'r')
    except:
        return "Script not found"
    return fopen.read()
    
@router.post("/scripts/uploadfile/", tags=["pb_pyscripts"])
async def create_upload_file(file: UploadFile = File(...)):
    save_upload_file(file, Path('/app/python_scripts/'+str(file.filename)))
    return {"filename": file.filename}
