# Import necessary modules
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Create a FastAPI application instance
app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Set up Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not set in .env")

genai.configure(api_key=gemini_api_key)

# Define a request model for the /chat endpoint
class ChatRequest(BaseModel):
    text: str

# Define a simple root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Define a health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Define the /chat endpoint using Gemini
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-pro
        response = model.generate_content(request.text)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
