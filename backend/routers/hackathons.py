from fastapi import APIRouter, HTTPException
import sheets_db
import uuid

router = APIRouter(
    prefix="/api/hackathons",
    tags=["hackathons"]
)

@router.get("/")
def get_all_hackathons():
    return sheets_db.get_all("Hackathons")

@router.get("/{hackathon_id}")
def get_hackathon(hackathon_id: str):
    h = sheets_db.get_by_id("Hackathons", 0, hackathon_id)
    if not h:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    return h

@router.post("/")
def create_hackathon(data: dict):
    if "hackathon_id" not in data:
        data["hackathon_id"] = f"HAC-{str(uuid.uuid4())[:8]}"
    return sheets_db.create_item("Hackathons", data)

@router.put("/{hackathon_id}")
def update_hackathon(hackathon_id: str, data: dict):
    res = sheets_db.update_item("Hackathons", 0, hackathon_id, data)
    if not res:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    return res

@router.delete("/{hackathon_id}")
def delete_hackathon(hackathon_id: str):
    success = sheets_db.delete_item("Hackathons", 0, hackathon_id)
    if not success:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    return {"status": "deleted"}


# Teams endpoints
@router.get("/teams/all")
def get_all_teams():
    return sheets_db.get_all("Teams")

@router.post("/teams/create")
def create_team(data: dict):
    if "team_id" not in data:
        data["team_id"] = f"TEAM-{str(uuid.uuid4())[:8]}"
    return sheets_db.create_item("Teams", data)

@router.put("/teams/{team_id}")
def update_team(team_id: str, data: dict):
    res = sheets_db.update_item("Teams", 0, team_id, data)
    if not res:
        raise HTTPException(status_code=404, detail="Team not found")
    return res

@router.get("/teams/hackathon/{hackathon_id}")
def get_teams_by_hackathon(hackathon_id: str):
    teams = sheets_db.get_all("Teams")
    return [t for t in teams if t.get("hackathon_id") == hackathon_id]
