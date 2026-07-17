import os

FRONTEND_DIR = r"../frontend/src/app/admin"
BACKEND_DIR = r"routers"

pages = {
    "users": """'use client';
import React, { useState, useEffect } from 'react';

export default function ManageUsers() {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);

  const fetchUsers = () => {
    setLoading(true);
    fetch(`http://localhost:8000/api/admin/users?skip=${page * 50}&limit=50`)
      .then(res => res.json())
      .then(data => { setUsers(data); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  };

  useEffect(() => { fetchUsers(); }, [page]);

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this user?')) return;
    try {
      await fetch(`http://localhost:8000/api/admin/users/${id}`, { method: 'DELETE' });
      fetchUsers();
    } catch (err) { console.error(err); }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Manage Users</h1>
      <div className="bg-foreground/5 rounded-xl border border-foreground/10 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-foreground/10 border-b border-foreground/10">
            <tr>
              <th className="p-4 font-semibold">Name</th>
              <th className="p-4 font-semibold">Email</th>
              <th className="p-4 font-semibold">Branch</th>
              <th className="p-4 font-semibold">Role</th>
              <th className="p-4 font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={5} className="p-8 text-center text-foreground/50">Loading users...</td></tr>
            ) : users.map((u: any) => (
              <tr key={u.id} className="border-b border-foreground/10 last:border-0 hover:bg-foreground/5">
                <td className="p-4 font-medium">{u.full_name}</td>
                <td className="p-4 text-foreground/70">{u.email}</td>
                <td className="p-4 text-foreground/70">{u.branch || 'N/A'}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${u.role === 'admin' ? 'bg-purple-500/20 text-purple-500' : 'bg-blue-500/20 text-blue-500'}`}>
                    {u.role}
                  </span>
                </td>
                <td className="p-4"><button onClick={() => handleDelete(u.id)} className="text-red-500 hover:underline">Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="p-4 border-t border-foreground/10 flex justify-between items-center bg-foreground/5">
          <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0} className="px-4 py-2 bg-foreground/10 rounded disabled:opacity-50">Previous</button>
          <span className="text-sm font-medium">Page {page + 1}</span>
          <button onClick={() => setPage(p => p + 1)} disabled={users.length < 50} className="px-4 py-2 bg-foreground/10 rounded disabled:opacity-50">Next</button>
        </div>
      </div>
    </div>
  );
}
""",
    "careers": """'use client';
import React, { useState, useEffect } from 'react';

export default function ManageCareers() {
  const [careers, setCareers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);

  const fetchCareers = () => {
    setLoading(true);
    fetch(`http://localhost:8000/api/careers/?skip=${page * 50}&limit=50`)
      .then(res => res.json())
      .then(data => { setCareers(data); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  };

  useEffect(() => { fetchCareers(); }, [page]);

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this career? This also deletes its roadmaps/mappings.')) return;
    try {
      await fetch(`http://localhost:8000/api/careers/${id}`, { method: 'DELETE' });
      fetchCareers();
    } catch (err) { console.error(err); }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Manage Careers</h1>
      <div className="bg-foreground/5 rounded-xl border border-foreground/10 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-foreground/10 border-b border-foreground/10">
            <tr>
              <th className="p-4 font-semibold">Name</th>
              <th className="p-4 font-semibold">Category</th>
              <th className="p-4 font-semibold">Salary (India)</th>
              <th className="p-4 font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={4} className="p-8 text-center text-foreground/50">Loading careers...</td></tr>
            ) : careers.map((c: any) => (
              <tr key={c.id} className="border-b border-foreground/10 last:border-0 hover:bg-foreground/5">
                <td className="p-4 font-medium">{c.name}</td>
                <td className="p-4 text-foreground/70">{c.category || 'Uncategorized'}</td>
                <td className="p-4 text-foreground/70">{c.india_salary || 'N/A'}</td>
                <td className="p-4"><button onClick={() => handleDelete(c.id)} className="text-red-500 hover:underline">Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="p-4 border-t border-foreground/10 flex justify-between items-center bg-foreground/5">
          <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0} className="px-4 py-2 bg-foreground/10 rounded disabled:opacity-50">Previous</button>
          <span className="text-sm font-medium">Page {page + 1}</span>
          <button onClick={() => setPage(p => p + 1)} disabled={careers.length < 50} className="px-4 py-2 bg-foreground/10 rounded disabled:opacity-50">Next</button>
        </div>
      </div>
    </div>
  );
}
""",
    "roadmaps": """'use client';
import React, { useState, useEffect } from 'react';

export default function ManageRoadmaps() {
  const [roadmaps, setRoadmaps] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);

  const fetchRoadmaps = () => {
    setLoading(true);
    fetch(`http://localhost:8000/api/roadmaps/?skip=${page * 50}&limit=50`)
      .then(res => res.json())
      .then(data => { setRoadmaps(data); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  };

  useEffect(() => { fetchRoadmaps(); }, [page]);

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this roadmap?')) return;
    try {
      await fetch(`http://localhost:8000/api/roadmaps/${id}`, { method: 'DELETE' });
      fetchRoadmaps();
    } catch (err) { console.error(err); }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Manage Roadmaps</h1>
      <div className="bg-foreground/5 rounded-xl border border-foreground/10 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-foreground/10 border-b border-foreground/10">
            <tr>
              <th className="p-4 font-semibold">Title</th>
              <th className="p-4 font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={2} className="p-8 text-center text-foreground/50">Loading roadmaps...</td></tr>
            ) : roadmaps.map((r: any) => (
              <tr key={r.id} className="border-b border-foreground/10 last:border-0 hover:bg-foreground/5">
                <td className="p-4 font-medium">{r.title}</td>
                <td className="p-4"><button onClick={() => handleDelete(r.id)} className="text-red-500 hover:underline">Delete</button></td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="p-4 border-t border-foreground/10 flex justify-between items-center bg-foreground/5">
          <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0} className="px-4 py-2 bg-foreground/10 rounded disabled:opacity-50">Previous</button>
          <span className="text-sm font-medium">Page {page + 1}</span>
          <button onClick={() => setPage(p => p + 1)} disabled={roadmaps.length < 50} className="px-4 py-2 bg-foreground/10 rounded disabled:opacity-50">Next</button>
        </div>
      </div>
    </div>
  );
}
"""
}

routers = {
    "admin.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    return {
        "users": db.query(models.User).count(),
        "branches": db.query(models.Branch).count(),
        "careers": db.query(models.Career).count(),
        "roadmaps": db.query(models.Roadmap).count()
    }

@router.get("/users")
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.created_at.desc()).offset(skip).limit(limit).all()
    return [{"id": u.id, "user_id": u.user_id, "full_name": u.full_name, "email": u.email, "mobile_number": u.mobile_number, "branch": u.branch, "college_name": u.college_name, "role": u.role, "created_at": u.created_at} for u in users]

@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"status": "deleted"}
""",
    "roadmaps.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db

router = APIRouter(prefix="/api/roadmaps", tags=["roadmaps"])

@router.get("/")
def get_roadmaps(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Roadmap).offset(skip).limit(limit).all()

@router.delete("/{roadmap_id}")
def delete_roadmap(roadmap_id: str, db: Session = Depends(get_db)):
    r = db.query(models.Roadmap).filter(models.Roadmap.id == roadmap_id).first()
    if not r: raise HTTPException(status_code=404, detail="Not found")
    db.delete(r)
    db.commit()
    return {"status": "deleted"}
""",
    "ui_elements.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db

router = APIRouter(prefix="/api/ui", tags=["ui_elements"])

@router.get("/buttons")
def get_buttons(db: Session = Depends(get_db)):
    return db.query(models.DynamicButton).all()

@router.post("/buttons")
def create_button(data: dict, db: Session = Depends(get_db)):
    btn = models.DynamicButton(**data)
    db.add(btn)
    db.commit()
    db.refresh(btn)
    return btn

@router.delete("/buttons/{btn_id}")
def delete_button(btn_id: str, db: Session = Depends(get_db)):
    btn = db.query(models.DynamicButton).filter(models.DynamicButton.id == btn_id).first()
    if btn:
        db.delete(btn)
        db.commit()
    return {"status": "deleted"}

@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    return db.query(models.Alert).all()

@router.post("/alerts")
def create_alert(data: dict, db: Session = Depends(get_db)):
    a = models.Alert(**data)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

@router.delete("/alerts/{a_id}")
def delete_alert(a_id: str, db: Session = Depends(get_db)):
    a = db.query(models.Alert).filter(models.Alert.id == a_id).first()
    if a:
        db.delete(a)
        db.commit()
    return {"status": "deleted"}
"""
}

# Create frontend pages
for page, code in pages.items():
    d = os.path.join(FRONTEND_DIR, page)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "page.tsx"), "w", encoding="utf-8") as f:
        f.write(code)

# Create backend routers
for name, code in routers.items():
    with open(os.path.join(BACKEND_DIR, name), "w", encoding="utf-8") as f:
        f.write(code)

print("✅ Successfully generated all missing frontend pages and backend routers!")
