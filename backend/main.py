from fastapi import FastAPI, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
import os
import shutil

from services.resume_parser import extract_text
from services.gemini_service import analyze_resume
from database.mongodb import application_collection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "ATS Backend Running"}

@app.post("/upload-resume")
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

@app.get("/applications")
async def get_applications():
    data = list(application_collection.find())

    for item in data:
        item["_id"] = str(item["_id"])

    return data

@app.put("/applications/{app_id}")
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