# HRMS-AI (Human Resource Management System - AI Services)

Welcome to the HRMS-AI repository. This service is a centralized AI microservice layer for the HRMS ecosystem, providing Applicant Tracking System (ATS) features, recruitment intelligence, and an AI HR Assistant.

---

## Project Architecture

This repository is organized as a monorepo containing the Python FastAPI backend and React frontend:

```
hrms-ai/
├── app/                        # Python FastAPI Backend
│   ├── main.py                 # Backend Entrypoint & Route registration
│   ├── ats/                    # ATS (Applicant Tracking System) Module
│   │   ├── routes.py           # ATS APIs (/upload-resume, /applications)
│   │   └── services/           
│   │       ├── resume_parser.py # PDF & DOCX text extractors
│   │       └── ats_service.py   # Resume evaluation & scoring logic
│   ├── assistant/              # AI Assistant Module
│   │   ├── routes.py           # Assistant chat & status routes
│   │   ├── prompts.py          # Assistant system prompts
│   │   ├── services.py         # Chat completion processors
│   │   └── schemas.py          # Pydantic schemas for request/response validation
│   ├── analytics/              # (Placeholder) HR Analytics Module
│   ├── reports/                # (Placeholder) AI Report Generation Module
│   ├── shared/                 # Shared Services and Utilities
│   │   ├── gemini.py           # Centralized LLM client (Groq / Gemini)
│   │   ├── database.py         # MongoDB client
│   │   ├── utils.py            # Shared utility helper functions
│   │   ├── auth.py             # Shared authentication helpers
│   │   └── prompts.py          # Common Prompt Templates
│   └── docs/                   # AI service documentation
├── frontend/                   # React Frontend (Vite)
│   ├── src/
│   │   ├── pages/              # Careers, Apply, and HR Dashboard pages
│   │   └── services/
│   ├── package.json            # Frontend dependencies
│   └── vite.config.js          # Vite configuration
├── requirements.txt            # Unified backend python dependencies
├── .env                        # Local environment settings
└── README.md                   # This documentation
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
# API Keys for AI Models
# Note: The original ATS service uses a Groq API key with the GEMINI_API_KEY environment variable.
# You can provide either a Groq API Key (starts with gsk_) or Google Gemini API Key.
GEMINI_API_KEY="your_api_key_here"
GROQ_API_KEY=""
```

---

## Local Setup

### 1. Prerequisites
- **Python**: Version 3.8 or higher
- **Node.js**: Version 18 or higher
- **MongoDB**: Running locally at `mongodb://localhost:27017`

### 2. Backend Setup
1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   The backend will be running at [http://localhost:8000](http://localhost:8000).

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The frontend will be running at [http://localhost:5173](http://localhost:5173).

---

## Deployment Process

For production deployment:
1. Set the production environment variables (e.g., `GEMINI_API_KEY`, MongoDB production connection string).
2. Build the production assets for the frontend:
   ```bash
   cd frontend
   ```
   ```bash
   npm run build
   ```
3. Run the FastAPI backend using a production-ready WSGI/ASGI server like `gunicorn` with `uvicorn` workers:
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   ```
