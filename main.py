from fastapi import FastAPI, Depends, HTTPException
import services, db_models, api_schemas
from db import get_db, engine
from sqlalchemy.orm import Session
from api_schemas import *

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/spots", response_model=list[Spot])
def get_all_spots(db: Session = Depends(get_db)):
    return services.get_all_spots(db)

@app.post("spots", response_model=Spot)
def create_spot(spot: SpotCreate, db: Session = Depends(get_db)):
    return create_spot(spot, db)