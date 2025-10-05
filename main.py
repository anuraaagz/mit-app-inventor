from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Name
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add_name")
def add_name(name: str, db: Session = Depends(get_db)):
    new_name = Name(name=name)
    db.add(new_name)
    db.commit()
    return {"message": "Name added successfully"}

@app.get("/get_names")
def get_names(db: Session = Depends(get_db)):
    names = db.query(Name).all()
    return {"names": [n.name for n in names]}
