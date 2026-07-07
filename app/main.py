from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.ats.routes import router as ats_router
from app.assistant.routes import router as assistant_router

app = FastAPI(title="HRMS AI Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register ATS routes (no prefix to maintain compatibility with the frontend)
app.include_router(ats_router)

# Register Assistant routes (prefixed with /assistant)
app.include_router(assistant_router)

# Live-reload trigger comment
@app.get("/")
def home():
    return {"message": "HRMS AI Service Running"}
