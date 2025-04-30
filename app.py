from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Optional: CORS settings to allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to VisaSwift API. It is running successfully."}

# Add additional endpoints here
# Example:
@app.get("/status")
def status_check():
    return {"status": "API is live and working properly!"}
