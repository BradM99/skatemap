from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import services
from api_schemas import *
from db import get_db

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/spots", response_model=list[Spot])
def get_all_spots(db: Session = Depends(get_db)):
    return services.get_all_spots(db)

@app.post("/spots", response_model=Spot)
def create_spots(spot: SpotCreate, db: Session = Depends(get_db)):
    return services.create_spot(db, spot)