from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Name
from typing import List

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JSON model for POST request
class NameRequest(BaseModel):
    name: str

# JSON model for GET response
class NamesResponse(BaseModel):
    names: List[str]

@app.post("/add_name")
def add_name(request: NameRequest, db: Session = Depends(get_db)):
    new_name = Name(name=request.name)
    db.add(new_name)
    db.commit()
    return JSONResponse(content={"message": "Name added successfully"})

@app.get("/get_names", response_model=NamesResponse)
def get_names(db: Session = Depends(get_db)):
    names = db.query(Name).all()
    return {"names": [n.name for n in names]}
