from fastapi import FastAPI
from app.services.character_generation_service import generate_character

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "hello from be"}

@app.get("/generate-desc/{description}")
def read_item(description: str):
    return generate_character(description)