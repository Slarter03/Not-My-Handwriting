import subprocess
import sqlite3

# Function to download the spaCy language model
def download_spacy_model():
    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])

# Function to initialize the database
def initialize_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # Create a table for student writing profiles
    c.execute('''CREATE TABLE IF NOT EXISTS student_writing_profiles (
                    id INTEGER PRIMARY KEY,
                    student_name TEXT NOT NULL,
                    sample_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

# Main script execution
if __name__ == '__main__':
    download_spacy_model()
    initialize_database('student_profiles.db')
