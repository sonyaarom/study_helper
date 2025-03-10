import json
import psycopg2
from psycopg2.extras import Json
from config import config

def create_table(conn):
    """Create the universities table if it doesn't exist."""
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS universities (
            id SERIAL PRIMARY KEY,
            university_id VARCHAR(255) UNIQUE NOT NULL,
            stk_name VARCHAR(255) NOT NULL,
            url TEXT,
            application_dates TEXT,
            entrance_test_date TEXT,
            entrance_test_online BOOLEAN,
            entrance_test_subjects TEXT,
            required_language_level VARCHAR(50),
            public BOOLEAN,
            hochschule_or_uni VARCHAR(20),
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()
        print("Table 'universities' created or already exists.")

def insert_university_data(conn, university_id, data):
    """Insert or update university data in the database."""
    with conn.cursor() as cur:
        # Check if university already exists
        cur.execute("SELECT id FROM universities WHERE university_id = %s", (university_id,))
        result = cur.fetchone()
        
        if result:
            # Update existing record
            cur.execute("""
            UPDATE universities SET 
                stk_name = %s,
                url = %s,
                application_dates = %s,
                entrance_test_date = %s,
                entrance_test_online = %s,
                entrance_test_subjects = %s,
                required_language_level = %s,
                public = %s,
                hochschule_or_uni = %s,
                notes = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE university_id = %s
            """, (
                data.get('stk_name', ''),
                data.get('url', ''),
                data.get('application_dates', ''),
                data.get('entrance_test_date', ''),
                data.get('entrance_test_online', False),
                data.get('entrance_test_subjects', ''),
                data.get('required_language_level', ''),
                data.get('public', False),
                data.get('hochschule_or_uni', ''),
                data.get('notes', ''),
                university_id
            ))
            print(f"Updated data for {university_id}")
        else:
            # Insert new record
            cur.execute("""
            INSERT INTO universities (
                university_id, stk_name, url, application_dates, entrance_test_date,
                entrance_test_online, entrance_test_subjects, required_language_level,
                public, hochschule_or_uni, notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                university_id,
                data.get('stk_name', ''),
                data.get('url', ''),
                data.get('application_dates', ''),
                data.get('entrance_test_date', ''),
                data.get('entrance_test_online', False),
                data.get('entrance_test_subjects', ''),
                data.get('required_language_level', ''),
                data.get('public', False),
                data.get('hochschule_or_uni', ''),
                data.get('notes', '')
            ))
            print(f"Inserted data for {university_id}")
        
        conn.commit()

def main():
    # Load the JSON data
    try:
        with open('universities_data.json', 'r', encoding='utf-8') as f:
            universities_data = json.load(f)
    except FileNotFoundError:
        print("Error: universities_data.json not found!")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON in universities_data.json!")
        return
    
    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname=config.db_name,
            user=config.db_user,
            password=config.db_password,
            host=config.db_host,
            port=config.db_port
        )
        print("Connected to PostgreSQL database")
        
        # Create table if it doesn't exist
        create_table(conn)
        
        # Insert or update data for each university
        for university_id, data in universities_data.items():
            insert_university_data(conn, university_id, data)
        
        print(f"Successfully processed {len(universities_data)} universities")
        
    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    main() 