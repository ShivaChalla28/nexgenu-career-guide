# Trigger reload for missing files
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import branches, careers, admin, roadmaps, ui_elements, auth, feedback

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NexGenU Backend API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_origin_regex="https://.*",  # Allows any Vercel/HTTPS domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(branches.router)
app.include_router(careers.router)
app.include_router(admin.router)
app.include_router(roadmaps.router)
app.include_router(ui_elements.router)
app.include_router(feedback.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to NexGenU API"}
