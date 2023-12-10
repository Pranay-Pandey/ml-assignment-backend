import datetime
from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel
from app.database import Base
from typing import Optional
# Create a Base class for declarative models

# Define the SQLAlchemy model
class Prediction(Base):
    __tablename__ = "predictions"

    id:Optional[int] = Column(Integer, primary_key=True, index=True)
    prompt = Column(String)
    label = Column(String)
    score = Column(String)
    user_id = Column(Integer)
    time = Column(DateTime, default=datetime.datetime.utcnow)
    
class Text(BaseModel):
    request: str
    when: str

class Prompt(BaseModel):
    prompt: str

class Users(Base):
    __tablename__ = "users"

    id:Optional[int] = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)