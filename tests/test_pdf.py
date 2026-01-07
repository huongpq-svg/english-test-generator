import os
import sys

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from pdf_generator import create_pdf

def test_create_pdf_mc(tmp_path):
    # Mock questions
    questions = [
        {"question": "Test Q1", "points": 50, "options": ["A", "B"], "answer": "A"},
        {"question": "Test Q2", "points": 50, "options": ["C", "D"], "answer": "C"},
    ]
    
    filename = tmp_path / "test_output.pdf"
    output = create_pdf(questions, str(filename))
    
    assert os.path.exists(output)
    assert os.path.getsize(output) > 0

def test_create_pdf_essay(tmp_path):
    questions = [
        {"question": "Essay Topic 1", "points": 100}
    ]
    
    filename = tmp_path / "essay_output.pdf"
    output = create_pdf(questions, str(filename))
    
    assert os.path.exists(output)
