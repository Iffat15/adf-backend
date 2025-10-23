# from fastapi import FastAPI
# from app.routes import pipelines   # 👈 Import the file where your routes are defined

# app = FastAPI()

# # 👇 Include the router
# app.include_router(pipelines.router, prefix="/pipelines", tags=["pipelines"])
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db_config import test_connection
from app.routes import scripts, run
from app.routes import pipelines
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
app.include_router(pipelines.router,prefix="/pipelines")

# Startup DB check
@app.on_event("startup")
async def startup_db_check():
    await test_connection()
