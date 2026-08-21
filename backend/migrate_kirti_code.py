import os
import sys
from sqlalchemy import text

# Add the backend directory to sys.path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

def run_migration():
    print("Running database migration...")
    
    with engine.begin() as conn:
        try:
            # Add kirti_code column
            conn.execute(text("ALTER TABLE scans ADD COLUMN kirti_code VARCHAR;"))
            print("Successfully added 'kirti_code' column to 'scans' table.")
            
            # Create index for fast searching
            conn.execute(text("CREATE INDEX ix_scans_kirti_code ON scans (kirti_code);"))
            print("Successfully created index on 'kirti_code'.")
        except Exception as e:
            if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                print("Column 'kirti_code' already exists.")
            else:
                print(f"Error running migration: {e}")

if __name__ == "__main__":
    run_migration()
