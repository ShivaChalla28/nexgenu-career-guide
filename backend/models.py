from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    mobile_number = Column(String)
    branch = Column(String)
    college_name = Column(String)
    graduation_year = Column(String)
    state = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    slug = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    icon = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    careers = relationship("BranchCareerMap", back_populates="branch")

from sqlalchemy import JSON

class Career(Base):
    __tablename__ = "careers"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    slug = Column(String, unique=True, index=True)
    category = Column(String, nullable=True, default="Core Careers")  # Core Careers | IT & Digital Careers | Government & PSU Careers
    overview = Column(Text, nullable=True)
    responsibilities = Column(JSON, nullable=True)
    who_can_apply = Column(Text, nullable=True)
    industry_demand = Column(String, nullable=True)
    future_scope = Column(Text, nullable=True)
    india_salary = Column(String, nullable=True)
    international_salary = Column(String, nullable=True)
    remote_opportunities = Column(String, nullable=True)
    growth_path = Column(JSON, nullable=True)
    
    branches = relationship("BranchCareerMap", back_populates="career")
    roadmaps = relationship("Roadmap", back_populates="career")

class BranchCareerMap(Base):
    __tablename__ = "branch_career_map"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    branch_id = Column(Uuid, ForeignKey("branches.id"))
    career_id = Column(Uuid, ForeignKey("careers.id"))

    branch = relationship("Branch", back_populates="careers")
    career = relationship("Career", back_populates="branches")

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    career_id = Column(Uuid, ForeignKey("careers.id"))
    title = Column(String)
    description = Column(Text, nullable=True)
    
    skills_matrix = Column(JSON, nullable=True)
    learning_plans = Column(JSON, nullable=True)
    learning_steps = Column(JSON, nullable=True)
    projects = Column(JSON, nullable=True)
    practice_questions = Column(JSON, nullable=True)
    certifications = Column(JSON, nullable=True)
    interview_prep = Column(JSON, nullable=True)
    readiness_checklist = Column(JSON, nullable=True)
    
    career = relationship("Career", back_populates="roadmaps")

class DynamicButton(Base):
    __tablename__ = "dynamic_buttons"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    icon = Column(String)
    color = Column(String)
    url = Column(String)
    placement = Column(String)
    target = Column(String, default="_blank")
    is_active = Column(Integer, default=1)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    type = Column(String) # placement, internship, hackathon, etc
    title = Column(String)
    message = Column(Text)
    priority = Column(String) # high, medium, low
    is_active = Column(Integer, default=1)

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(String, index=True) # ID from Google Sheets
    name = Column(String)
    branch = Column(String, nullable=True)
    college = Column(String, nullable=True)
    rating = Column(Integer, default=5)
    text = Column(Text)
    is_approved = Column(Integer, default=0) # 0 = pending, 1 = approved
    created_at = Column(DateTime, default=datetime.utcnow)

class Ad(Base):
    __tablename__ = "ads"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    link_url = Column(String, nullable=True)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
