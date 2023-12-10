from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional, Annotated
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from app.models import Prediction, Prompt, Users
from app.database import Base, engine, SessionLocal
import app.inference as inference
import datetime
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from app import auth
from app.auth import get_current_user, Token

load_dotenv()

app = FastAPI()
app.include_router(auth.router)
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the table
Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/")
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"User": user}


@app.post("/predict")
async def predict(text: Prompt, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = inference.sentiment_analysis(text.prompt)
    label = result[0]["label"]
    score = str(result[0]["score"])

    if table_entry(db, str(text.prompt), str(label), str(score), user["id"]):
        print("table entry successful")
    else:
        print("table entry failed")

    return result

def table_entry(db: Session, prompt_: str, label_: str, score_: str, user_id_: int):
    try:
        prediction = Prediction(prompt=prompt_, label=label_, score=score_, user_id=user_id_)
        db.add(prediction)
        db.commit()
        return True
    except Exception as e:
        print("Error: ", e)
        return False

    
@app.get("/data")
async def get_users( db: db_dependency, user: user_dependency):
    if user is None: 
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try: 
        predictions = db.query(Prediction).filter(Prediction.user_id==user["id"]).all()
        return predictions
    finally:
        db.close()