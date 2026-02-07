from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, Subject

app = FastAPI(title="Smart Study Planner")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Smart Study Planner API is running"}

@app.post("/subjects/")
def add_subject(name: str, priority: str, db: Session = Depends(get_db)):
    subject = Subject(name=name, priority=priority)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject

@app.get("/subjects/")
def get_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()

@app.get("/study-plan/")
def study_plan(total_hours: int, db: Session = Depends(get_db)):
    subjects = db.query(Subject).all()
    plan = []

    for subject in subjects:
        if subject.priority.lower() == "high":
            hours = total_hours * 0.5
        elif subject.priority.lower() == "medium":
            hours = total_hours * 0.3
        else:
            hours = total_hours * 0.2

        plan.append({
            "subject": subject.name,
            "priority": subject.priority,
            "hours": round(hours, 1)
        })

    return plan