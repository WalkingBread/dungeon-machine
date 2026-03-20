import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import session

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router)

PORT = 8000

if __name__ == '__main__':
    uvicorn.run(app, port=PORT)