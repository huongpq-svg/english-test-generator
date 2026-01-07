# 🇬🇧 English Test Generator

A powerful, full-stack application to generate English knowledge tests for Grades 1-10. Built with **FastAPI** (Backend) and **Streamlit** (Frontend).

## 🚀 Features

*   **Grade Selection**: Tailored content for Grades 1 through 10.
*   **Flexible Test Types**:
    *   Multiple Choice
    *   Essay
    *   Combination (Adjustable ratio)
*   **Dynamic Generation**: Questions are procedurally generated and stored in a database (1000+ questions).
*   **PDF Export**: Download professional-looking test PDFs with proper formatting and UTF-8 support.
*   **Architecture**: Robust 3-tier architecture (SQLite \u2192 FastAPI \u2192 Streamlit).

## 🛠️ Tech Stack

*   **Frontend**: Streamlit
*   **Backend**: FastAPI, Uvicorn
*   **Database**: SQLite, SQLAlchemy
*   **PDF Generation**: FPDF2
*   **Testing**: Pytest, HTTPX

## 🏃‍♂️ How to Run

The application is split into two parts. You need to run both the Backend and the Frontend.

### Prerequisites
*   Python 3.8+
*   Pip

### 1. Setup & Install
First, install the required dependencies:
```bash
pip install -r requirements.txt
# OR manually
pip install fastapi uvicorn sqlalchemy requests streamlit fpdf2 pytest httpx
```

### 2. Start the Backend
This script starts the API server on port 8000 and automatically seeds the database if needed.
```bash
sh run_backend.sh
```

### 3. Start the Frontend
Open a new terminal and run:
```bash
sh run_frontend.sh
```
Access the app at `http://localhost:8501`.

## 🧪 Running Tests
To run the automated test suite:
```bash
sh run_tests.sh
```

## 📂 Project Structure
```
.
├── src/
│   ├── api.py           # FastAPI Backend
│   ├── app.py           # Streamlit Frontend
│   ├── database.py      # Database Connection
│   ├── models.py        # SQLAlchemy Models
│   ├── pdf_generator.py # PDF Creation Logic
│   ├── questions.py     # Question Generation Logic
│   └── seed.py          # Database Seeder
├── tests/               # Automated Tests
├── questions.db         # SQLite Database
├── run_backend.sh       # Helper script for Backend
├── run_frontend.sh      # Helper script for Frontend
└── README.md
```

## 📝 License
Copyright © Phạm Quang Hương
