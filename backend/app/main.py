from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import query, upload

app = FastAPI()

# Enable CORS (VERY IMPORTANT for React!!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(query.router)
app.include_router(upload.router)
