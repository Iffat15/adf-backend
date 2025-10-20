from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db_config import test_connection
from app.routes import scripts, run

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(scripts.router, prefix="/scripts")
app.include_router(run.router, prefix="/run")

# Startup DB check
@app.on_event("startup")
async def startup_db_check():
    await test_connection()
