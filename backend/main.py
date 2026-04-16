from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import spacy  # or other NLP libraries

# Initialize FastAPI
app = FastAPI()

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('student_writings.db')
    conn.row_factory = sqlite3.Row
    return conn

# Pydantic models
class StudentProfile(BaseModel):
    student_id: int
    name: str
    writing_style: str

class Writing(BaseModel):
    student_id: int
    text: str

# Create the database and student table if not exists
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                writing_style TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS writings (
                id INTEGER PRIMARY KEY,
                student_id INTEGER,
                text TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
    conn.close()

# FastAPI startup event to initialize the DB
@app.on_event("startup")
def startup():
    init_db()

# API to create student profile
@app.post('/students/')
def create_student(profile: StudentProfile):
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO students (name, writing_style)
            VALUES (?, ?)
        ''', (profile.name, profile.writing_style))
    return {"message": "Student profile created."}

# API to upload student writing
@app.post('/writings/')
def upload_writing(writing: Writing):
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO writings (student_id, text)
            VALUES (?, ?)
        ''', (writing.student_id, writing.text))
    return {"message": "Writing uploaded."}

# API to compare writing styles (not implemented)
@app.get('/compare/')
def compare_writing_style(student_id1: int, student_id2: int):
    # Placeholder for actual NLP comparison logic
    return {"message": "Comparing writing styles..."}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)