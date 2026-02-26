from fastapi import FastAPI

from api import spots

app = FastAPI()

app.include_router(spots.router)

@app.get("/")
def root():
    return {"message": "API is running"}
