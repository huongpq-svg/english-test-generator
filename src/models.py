from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Integer, index=True)
    category = Column(String, index=True) # "Beginner", "Intermediate", "Advanced"
    type = Column(String, index=True) # "Multiple Choice", "Essay"
    subtype = Column(String) # "vocab", "grammar", "essay"
    
    question_text = Column(Text, nullable=False)
    answer = Column(Text, nullable=True) # Null for Essay
    options = Column(JSON, nullable=True) # JSON list for MC options
