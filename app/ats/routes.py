import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, Body
from bson import ObjectId

from app.ats.services.resume_parser import extract_text
from app.ats.services.ats_service import analyze_resume
from app.shared.database import application_collection

router = APIRouter()

UPLOAD_FOLDER = "uploads/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload-resume")
async def upload_resume(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    position: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resume_text = extract_text(file_path)

        analysis = analyze_resume(resume_text)

        document = {
            "name": name,
            "email": email,
            "phone": phone,
            "position": position,
            "filename": file.filename,
            "resume_text": resume_text,
            "analysis": analysis,
            "status": "pending"
        }

        result = application_collection.insert_one(document)

        return {
            "message": "Resume uploaded successfully",
            "id": str(result.inserted_id)
        }

    except Exception as e:
        return {
            "message": "Upload failed",
            "error": str(e)
        }

@router.get("/applications")
async def get_applications():
    data = list(application_collection.find())

    for item in data:
        item["_id"] = str(item["_id"])

    return data

@router.put("/applications/{app_id}")
async def update_status(app_id: str, body: dict = Body(...)):
    new_status = body.get("status")

    if not new_status:
        return {"error": "status is required"}

    result = application_collection.update_one(
        {"_id": ObjectId(app_id)},
        {"$set": {"status": new_status}}
    )

    if result.modified_count == 0:
        return {"message": "No document updated"}

    return {"message": "Status updated successfully"}

@router.post("/ats/screen")
async def screen_resume(body: dict = Body(...)):
    file_path = body.get("file_path")
    if not file_path:
        return {"success": False, "error": "file_path is required"}
    
    try:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File does not exist: {file_path}"}
            
        resume_text = extract_text(file_path)
        analysis = analyze_resume(resume_text)
        return {"success": True, "analysis": analysis}
    except Exception as e:
        return {"success": False, "error": str(e)}
