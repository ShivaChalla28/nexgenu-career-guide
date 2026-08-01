from fastapi import APIRouter, HTTPException
import sheets_db
import uuid

router = APIRouter(
    prefix="/api/incubation",
    tags=["incubation"]
)

@router.get("/ideas")
def get_all_ideas():
    return sheets_db.get_all("StartupIdeas")

@router.get("/ideas/{idea_id}")
def get_idea(idea_id: str):
    idea = sheets_db.get_by_id("StartupIdeas", 0, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return idea

@router.post("/ideas")
def create_idea(data: dict):
    if "idea_id" not in data:
        data["idea_id"] = f"IDEA-{str(uuid.uuid4())[:8]}"
    return sheets_db.create_item("StartupIdeas", data)

@router.put("/ideas/{idea_id}")
def update_idea(idea_id: str, data: dict):
    res = sheets_db.update_item("StartupIdeas", 0, idea_id, data)
    if not res:
        raise HTTPException(status_code=404, detail="Idea not found")
    return res

@router.delete("/ideas/{idea_id}")
def delete_idea(idea_id: str):
    success = sheets_db.delete_item("StartupIdeas", 0, idea_id)
    if not success:
        raise HTTPException(status_code=404, detail="Idea not found")
    return {"status": "deleted"}
