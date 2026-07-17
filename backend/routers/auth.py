"""
routers/auth.py
Authentication using Google Sheets as the user database.
Register → saves to Sheets + sends welcome email
Login    → reads from Sheets + verifies password
"""

from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from passlib.context import CryptContext
import schemas
from sheets_db import create_user, get_user_by_email, get_user_by_id
from integrations import send_welcome_email
import uuid
import re

router = APIRouter(prefix="/api/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# ─── Register ─────────────────────────────────────────────────────────────────
@router.post("/register")
def register(user: schemas.UserCreate, background_tasks: BackgroundTasks):
    # Duplicate email check
    existing = get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = f"NXG-{str(uuid.uuid4()).split('-')[1].upper()}"

    new_user = create_user({
        "user_id":         user_id,
        "full_name":       user.full_name,
        "email":           user.email,
        "mobile_number":   user.mobile_number,
        "branch":          user.branch,
        "college_name":    user.college_name,
        "graduation_year": user.graduation_year,
        "state":           user.state,
        "hashed_password": hash_password(user.password),
        "role":            "user",
    })

    # Welcome email in background
    background_tasks.add_task(
        send_welcome_email,
        user.email,
        user.full_name,
        user_id,
        user.branch,
    )

    return {
        "message": "Registration successful",
        "user": {
            "user_id":   user_id,
            "full_name": user.full_name,
            "email":     user.email,
            "branch":    user.branch,
            "role":      "user",
        }
    }


# ─── Login ────────────────────────────────────────────────────────────────────
@router.post("/login")
def login(user_credentials: schemas.UserLogin):
    identifier = user_credentials.identifier.strip()
    is_email   = bool(re.match(r"[^@]+@[^@]+\.[^@]+", identifier))

    user = get_user_by_email(identifier) if is_email else get_user_by_id(identifier)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(user_credentials.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return {
        "message": "Login successful",
        "user": {
            "user_id":   user["user_id"],
            "full_name": user["full_name"],
            "email":     user["email"],
            "branch":    user["branch"],
            "role":      user.get("role", "user"),
        }
    }
