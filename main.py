from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()

# Simulated in-memory DB
users = {}
applications = {}

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

@app.get("/")
def read_root():
    return {"message": "VisaSwift API Running!"}

# --- User Routes ---

@app.post("/user/register")
def register(user: UserRegister):
    if user.username in users:
        return {"error": "User already exists"}
    users[user.username] = user.password
    return {"message": "User registered"}

@app.post("/user/login")
def login(user: UserLogin):
    if users.get(user.username) != user.password:
        return {"error": "Invalid credentials"}
    return {"message": "Login successful"}

@app.post("/user/apply")
def apply_visa(application: VisaApplication):
    visa_id = str(uuid.uuid4())
    applications[visa_id] = {
        "info": application,
        "status": "Pending",
        "doc_uploaded": False,
        "verified": False
    }
    return {"visa_id": visa_id, "message": "Application submitted"}

@app.post("/user/upload/{visa_id}")
def upload_doc(visa_id: str, file: UploadFile = File(...)):
    if visa_id not in applications:
        return {"error": "Invalid visa ID"}
    applications[visa_id]["doc_uploaded"] = True
    return {"message": f"Document uploaded for {visa_id}"}

@app.get("/user/status/{visa_id}")
def check_status(visa_id: str):
    if visa_id not in applications:
        return {"error": "Visa ID not found"}
    return {"status": applications[visa_id]["status"]}

# --- Admin Routes ---

@app.get("/admin/applications")
def list_applications():
    return applications

@app.post("/admin/verify/{visa_id}")
def verify_doc(visa_id: str):
    if visa_id not in applications:
        return {"error": "Invalid visa ID"}
    if not applications[visa_id]["doc_uploaded"]:
        return {"error": "Document not uploaded"}
    applications[visa_id]["verified"] = True
    return {"message": "Documents verified"}

@app.post("/admin/approve/{visa_id}")
def approve_app(visa_id: str):
    if visa_id not in applications:
        return {"error": "Invalid visa ID"}
    if not applications[visa_id]["verified"]:
        return {"error": "Documents not verified"}
    applications[visa_id]["status"] = "Approved"
    return {"message": "Application approved"}
