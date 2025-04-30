from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(
    title="VisaSwift API 🛂",
    description="FastAPI backend for the VisaSwift application. Submit, track, and verify visa applications.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# In-memory simulated database
users = {}
applications = {}

# -------------------- Models --------------------

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class VisaApplication(BaseModel):
    full_name: str
    passport_number: str
    travel_date: str
    destination: str

# -------------------- Root Route --------------------

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "VisaSwift API is up and running!"}

# -------------------- User Routes --------------------

@app.post("/user/register", tags=["User"], summary="Register a new user")
def register(user: UserRegister):
    if user.username in users:
        return {"error": "User already exists"}
    users[user.username] = user.password
    return {"message": "User registered"}

@app.post("/user/login", tags=["User"], summary="Login for existing user")
def login(user: UserLogin):
    if users.get(user.username) != user.password:
        return {"error": "Invalid credentials"}
    return {"message": "Login successful"}

@app.post("/user/apply", tags=["User"], summary="Apply for a visa")
def apply_visa(application: VisaApplication):
    visa_id = str(uuid.uuid4())
    applications[visa_id] = {
        "info": application,
        "status": "Pending",
        "doc_uploaded": False,
        "verified": False
    }
    return {"visa_id": visa_id, "message": "Application submitted"}

@app.post("/user/upload/{visa_id}", tags=["User"], summary="Upload document for a visa application")
def upload_doc(visa_id: str, file: UploadFile = File(...)):
    if visa_id not in applications:
        return {"error": "Invalid visa ID"}
    applications[visa_id]["doc_uploaded"] = True
    return {"message": f"Document uploaded for {visa_id}"}

@app.get("/user/status/{visa_id}", tags=["User"], summary="Check visa application status")
def check_status(visa_id: str):
    if visa_id not in applications:
        return {"error": "Visa ID not found"}
    return {"status": applications[visa_id]["status"]}

# -------------------- Admin Routes --------------------

@app.get("/admin/applications", tags=["Admin"], summary="View all visa applications")
def list_applications():
    return applications

@app.post("/admin/verify/{visa_id}", tags=["Admin"], summary="Verify uploaded document for a visa")
def verify_doc(visa_id: str):
    if visa_id not in applications:
        return {"error": "Invalid visa ID"}
    if not applications[visa_id]["doc_uploaded"]:
        return {"error": "Document not uploaded"}
    applications[visa_id]["verified"] = True
    return {"message": "Documents verified"}

@app.post("/admin/approve/{visa_id}", tags=["Admin"], summary="Approve a verified visa application")
def approve_app(visa_id: str):
    if visa_id not in applications:
        return {"error": "Invalid visa ID"}
    if not applications[visa_id]["verified"]:
        return {"error": "Documents not verified"}
    applications[visa_id]["status"] = "Approved"
    return {"message": "Application approved"}
