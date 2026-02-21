import sqlite3
import csv
import os

DB_FILE = 'cell-count.db'
CSV_FILE = 'cell-count.csv'

def init_db(conn):
    """Initialize database schema."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # subjects
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id TEXT PRIMARY KEY,
        project_id TEXT,
        condition TEXT,
        age INTEGER,
        sex TEXT,
        treatment TEXT,
        response TEXT
    );
    ''')
    
    # samples
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS samples (
        sample_id TEXT PRIMARY KEY,
        subject_id TEXT,
        sample_type TEXT,
        time_from_treatment_start INTEGER,
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    );
    ''')
    
    # cell counts
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cell_counts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sample_id TEXT UNIQUE,
        b_cell INTEGER,
        cd8_t_cell INTEGER,
        cd4_t_cell INTEGER,
        nk_cell INTEGER,
        monocyte INTEGER,
        FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
    );
    ''')
    conn.commit()

def load_data(conn):
    # load data from csv and add to database
    cursor = conn.cursor()
    
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found.")
        return

    with open(CSV_FILE, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # insert subject data
            cursor.execute('''
            INSERT OR IGNORE INTO subjects (subject_id, project_id, condition, age, sex, treatment, response)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['subject'], 
                row['project'], 
                row['condition'], 
                int(row['age']) if row['age'] else None, 
                row['sex'], 
                row['treatment'], 
                row['response'] if row['response'] else None
            ))
            
            # insert sample data
            cursor.execute('''
            INSERT OR IGNORE INTO samples (sample_id, subject_id, sample_type, time_from_treatment_start)
            VALUES (?, ?, ?, ?)
            ''', (
                row['sample'],
                row['subject'],
                row['sample_type'],
                int(row['time_from_treatment_start']) if row['time_from_treatment_start'] else None
            ))
            
            # insert cell counts data
            cursor.execute('''
            INSERT OR IGNORE INTO cell_counts (sample_id, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row['sample'],
                int(row['b_cell']) if row['b_cell'] else None,
                int(row['cd8_t_cell']) if row['cd8_t_cell'] else None,
                int(row['cd4_t_cell']) if row['cd4_t_cell'] else None,
                int(row['nk_cell']) if row['nk_cell'] else None,
                int(row['monocyte']) if row['monocyte'] else None
            ))

    conn.commit()

def main():
    """Initialize database and load data from CSV."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    conn = sqlite3.connect(DB_FILE)
    try:
        init_db(conn)
        load_data(conn)
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM subjects")
        cursor.execute("SELECT COUNT(*) FROM samples")
        cursor.execute("SELECT COUNT(*) FROM cell_counts")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
