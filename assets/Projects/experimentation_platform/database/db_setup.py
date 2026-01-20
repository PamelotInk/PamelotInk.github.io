import sqlite3
import os

# Path to database
DB_PATH = os.path.join('data', 'experiments.db')

def init_database():
    """Initialize database with schema"""
    
    # Create connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("📊 Creating database tables...")
    
    # Create experiments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            experiment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_name TEXT NOT NULL,
            description TEXT,
            start_date DATE NOT NULL,
            end_date DATE,
            status TEXT DEFAULT 'running',
            hypothesis TEXT,
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create variants table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS variants (
            variant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id INTEGER,
            variant_name TEXT,
            description TEXT,
            traffic_allocation REAL DEFAULT 50.00,
            FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
        )
    """)
    
    # Create experiment metrics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiment_metrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            experiment_id INTEGER,
            variant_id INTEGER,
            date DATE NOT NULL,
            impressions INTEGER DEFAULT 0,
            conversions INTEGER DEFAULT 0,
            revenue REAL DEFAULT 0.00,
            unique_users INTEGER DEFAULT 0,
            FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id),
            FOREIGN KEY (variant_id) REFERENCES variants(variant_id)
        )
    """)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("✅ Database created successfully!")
    print(f"📁 Location: {os.path.abspath(DB_PATH)}")

if __name__ == "__main__":
    init_database()