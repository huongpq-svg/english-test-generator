import sys
import os

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from database import SessionLocal
from models import Question
from sqlalchemy import func

def inspect():
    db = SessionLocal()
    
    print("="*40)
    print("      DATABASE INSPECTION")
    print("="*40)
    
    # 1. Total Count
    total = db.query(Question).count()
    print(f"\nTotal Questions in DB: {total}")
    
    # 2. Breakdown by Grade
    print("\n--- Breakdown by Grade ---")
    grade_counts = db.query(Question.grade, func.count(Question.id)).group_by(Question.grade).all()
    for grade, count in grade_counts:
        print(f"Grade {grade}: {count} questions")
        
    # 3. Breakdown by Type
    print("\n--- Breakdown by Category ---")
    cat_counts = db.query(Question.category, func.count(Question.id)).group_by(Question.category).all()
    for cat, count in cat_counts:
        print(f"{cat}: {count} questions")

    # 4. View Samples
    print("\n--- Sample Questions (First 5) ---")
    samples = db.query(Question).limit(5).all()
    for q in samples:
        print(f"ID: {q.id} | Grade: {q.grade} | Type: {q.type}")
        print(f"Q: {q.question_text}")
        print(f"A: {q.answer}")
        print("-" * 20)
        
    db.close()

if __name__ == "__main__":
    inspect()
