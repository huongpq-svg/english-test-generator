from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from contextlib import asynccontextmanager
import random

from database import get_db, init_db
from models import Question

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Init DB
    init_db()
    yield
    # Shutdown: Clean up if needed (nothing for now)

app = FastAPI(lifespan=lifespan)

# Pydantic models for response
class QuestionOut(BaseModel):
    id: int
    grade: int
    type: str
    question_text: str
    answer: Optional[str] = None
    options: Optional[List[str]] = None
    points: int = 0

    model_config = ConfigDict(from_attributes=True)

@app.get("/generate-test", response_model=List[QuestionOut])
def generate_test_api(
    grade: int,
    count: int,
    test_type: str, # "Multiple Choice", "Essay", "Combination"
    ratio: float = 0.7,
    db: Session = Depends(get_db)
):
    questions = []
    
    if test_type == "Multiple Choice":
        mc_count = count
        essay_count = 0
    elif test_type == "Essay":
        mc_count = 0
        essay_count = count
    else:
        mc_count = int(count * ratio)
        essay_count = count - mc_count
        
    # Fetch MC
    if mc_count > 0:
        mc_qs = db.query(Question).filter(
            Question.grade == grade, 
            Question.type == "Multiple Choice"
        ).order_by(func.random()).limit(mc_count).all()
        questions.extend(mc_qs)
        
    # Fetch Essay
    if essay_count > 0:
        essay_qs = db.query(Question).filter(
            Question.grade == grade, 
            Question.type == "Essay"
        ).order_by(func.random()).limit(essay_count).all()
        questions.extend(essay_qs)
        
    # Assign points
    if not questions:
        return []

    total_points = 100
    base_points = total_points // len(questions)
    remainder = total_points % len(questions)
    
    results = []
    for i, q in enumerate(questions):
        # Convert SQLAlchemy model to dict-like structure with points
        # usage of Pydantic model requires standard dict or object
        # We attach 'points' dynamically to the object logic or wrapper
        
        q_out = QuestionOut(
            id=q.id,
            grade=q.grade,
            type=q.type,
            question_text=q.question_text,
            answer=q.answer,
            options=q.options,
            points=base_points + (1 if i < remainder else 0)
        )
        results.append(q_out)
        
    return results

@app.get("/health")
def health():
    return {"status": "ok"}
