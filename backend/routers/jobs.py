from fastapi import APIRouter, HTTPException
import sheets_db
import uuid

router = APIRouter(
    prefix="/api/jobs",
    tags=["jobs"]
)

@router.get("/")
def get_all_jobs():
    return sheets_db.get_all("Jobs")

@router.get("/{job_id}")
def get_job(job_id: str):
    job = sheets_db.get_by_id("Jobs", 0, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/")
def create_job(data: dict):
    if "job_id" not in data:
        data["job_id"] = f"JOB-{str(uuid.uuid4())[:8]}"
    return sheets_db.create_item("Jobs", data)

@router.put("/{job_id}")
def update_job(job_id: str, data: dict):
    res = sheets_db.update_item("Jobs", 0, job_id, data)
    if not res:
        raise HTTPException(status_code=404, detail="Job not found")
    return res

@router.delete("/{job_id}")
def delete_job(job_id: str):
    success = sheets_db.delete_item("Jobs", 0, job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": "deleted"}

# Internships endpoints under the same router
@router.get("/internships/all")
def get_all_internships():
    return sheets_db.get_all("Internships")

@router.get("/internships/{internship_id}")
def get_internship(internship_id: str):
    intern = sheets_db.get_by_id("Internships", 0, internship_id)
    if not intern:
        raise HTTPException(status_code=404, detail="Internship not found")
    return intern

@router.post("/internships/create")
def create_internship(data: dict):
    if "internship_id" not in data:
        data["internship_id"] = f"INT-{str(uuid.uuid4())[:8]}"
    return sheets_db.create_item("Internships", data)

@router.put("/internships/{internship_id}")
def update_internship(internship_id: str, data: dict):
    res = sheets_db.update_item("Internships", 0, internship_id, data)
    if not res:
        raise HTTPException(status_code=404, detail="Internship not found")
    return res

@router.delete("/internships/{internship_id}")
def delete_internship(internship_id: str):
    success = sheets_db.delete_item("Internships", 0, internship_id)
    if not success:
        raise HTTPException(status_code=404, detail="Internship not found")
    return {"status": "deleted"}

# Applications endpoints
@router.post("/apply")
def apply_to_job(data: dict):
    if "app_id" not in data:
        data["app_id"] = f"APP-{str(uuid.uuid4())[:8]}"
    return sheets_db.create_item("Applications", data)

@router.get("/applications/all")
def get_all_applications():
    return sheets_db.get_all("Applications")
