from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    email: str
    mobile_number: str
    branch: str
    college_name: str
    graduation_year: str
    state: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    identifier: str
    password: str

class User(UserBase):
    id: UUID
    user_id: str
    role: str
    created_at: datetime
    class Config:
        from_attributes = True

class BranchBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None

class BranchCreate(BranchBase):
    pass

class Branch(BranchBase):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class CareerBase(BaseModel):
    name: str
    slug: str
    overview: Optional[str] = None
    category: Optional[str] = None          # Core Careers | IT & Digital Careers | Government & PSU Careers
    india_salary: Optional[str] = None
    industry_demand: Optional[str] = None
    avg_salary: Optional[str] = None
    demand: Optional[str] = None

class CareerCreate(CareerBase):
    pass

class Career(CareerBase):
    id: UUID
    class Config:
        from_attributes = True

class FeedbackBase(BaseModel):
    rating: int
    text: str

class FeedbackSubmit(FeedbackBase):
    user_id: str
    name: str
    branch: Optional[str] = None
    college: Optional[str] = None

class Feedback(FeedbackBase):
    id: UUID
    user_id: str
    name: str
    branch: Optional[str] = None
    college: Optional[str] = None
    is_approved: int
    created_at: datetime
    class Config:
        from_attributes = True
