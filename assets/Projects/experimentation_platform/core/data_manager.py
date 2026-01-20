import sqlite3
import pandas as pd
from datetime import date
from typing import List, Dict
import os

DB_PATH = os.path.join('data', 'experiments.db')

class ExperimentDataManager:
    """Handles all database operations"""
    
    def __init__(self):
        self.db_path = DB_PATH
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def create_experiment(
        self,
        name: str,
        description: str,
        hypothesis: str,
        start_date: date,
        created_by: str,
        variants: List[Dict]
    ) -> int:
        """Create a new experiment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Normalize date to ISO string to avoid sqlite3 default date adapter
        # deprecation in Python 3.12+. Store dates as ISO-formatted text.
        start_date_val = start_date.isoformat() if hasattr(start_date, 'isoformat') else start_date

        # Insert experiment
        cursor.execute("""
            INSERT INTO experiments 
            (experiment_name, description, hypothesis, start_date, created_by)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, hypothesis, start_date_val, created_by))
        
        experiment_id = cursor.lastrowid
        
        # Insert variants
        for variant in variants:
            cursor.execute("""
                INSERT INTO variants 
                (experiment_id, variant_name, description, traffic_allocation)
                VALUES (?, ?, ?, ?)
            """, (
                experiment_id,
                variant['name'],
                variant.get('description', ''),
                variant['allocation']
            ))
        
        conn.commit()
        conn.close()
        
        return experiment_id
    
    def get_active_experiments(self) -> pd.DataFrame:
        """Get all running experiments"""
        query = """
            SELECT 
                e.experiment_id,
                e.experiment_name,
                e.description,
                e.start_date,
                e.status,
                e.created_by,
                COUNT(DISTINCT v.variant_id) as variant_count
            FROM experiments e
            LEFT JOIN variants v ON e.experiment_id = v.experiment_id
            WHERE e.status = 'running'
            GROUP BY e.experiment_id
            ORDER BY e.start_date DESC
        """

        conn = self.get_connection()
        # Parse the start_date column as a date/time when loading into a DataFrame
        df = pd.read_sql(query, conn, parse_dates=['start_date'])
        conn.close()

        return df
    
    def get_experiment_results(self, experiment_id: int) -> pd.DataFrame:
        """Get aggregated results for an experiment"""
        query = """
            SELECT 
                v.variant_name,
                COALESCE(SUM(em.impressions), 0) as total_impressions,
                COALESCE(SUM(em.conversions), 0) as total_conversions,
                COALESCE(SUM(em.revenue), 0) as total_revenue,
                COUNT(DISTINCT em.date) as days_running
            FROM variants v
            LEFT JOIN experiment_metrics em ON v.variant_id = em.variant_id
            WHERE v.experiment_id = ?
            GROUP BY v.variant_id, v.variant_name
            ORDER BY v.variant_name
        """
        
        conn = self.get_connection()
        df = pd.read_sql(query, conn, params=(experiment_id,))
        conn.close()
        
        return df
    
    def log_metrics(
        self,
        experiment_id: int,
        variant_name: str,
        date_val: date,
        impressions: int,
        conversions: int,
        revenue: float
    ):
        """Log daily metrics for a variant"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get variant_id
        cursor.execute("""
            SELECT variant_id FROM variants 
            WHERE experiment_id = ? AND variant_name = ?
        """, (experiment_id, variant_name))
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            raise ValueError(f"Variant '{variant_name}' not found for experiment {experiment_id}")
        
        variant_id = result[0]
        
        # Normalize date to ISO string to avoid sqlite3 default date adapter
        date_val_norm = date_val.isoformat() if hasattr(date_val, 'isoformat') else date_val

        # Insert metrics (store date as ISO-formatted text)
        cursor.execute("""
            INSERT INTO experiment_metrics 
            (experiment_id, variant_id, date, impressions, conversions, revenue)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (experiment_id, variant_id, date_val_norm, impressions, conversions, revenue))
        
        conn.commit()
        conn.close()
    
    def complete_experiment(self, experiment_id: int):
        """Mark experiment as completed"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE experiments 
            SET status = 'completed', end_date = date('now')
            WHERE experiment_id = ?
        """, (experiment_id,))
        
        conn.commit()
        conn.close()


# Test it
if __name__ == "__main__":
    print("💾 Testing Data Manager...\n")
    
    dm = ExperimentDataManager()
    
    # Create a test experiment
    print("Creating test experiment...")
    exp_id = dm.create_experiment(
        name="Homepage Hero Test",
        description="Testing new hero image",
        hypothesis="New image will increase signups by 10%",
        start_date=date.today(),
        created_by="test@company.com",
        variants=[
            {'name': 'control', 'allocation': 50, 'description': 'Current image'},
            {'name': 'variant_a', 'allocation': 50, 'description': 'New image'}
        ]
    )
    
    print(f"✅ Created experiment ID: {exp_id}\n")
    
    # Log some test metrics
    print("Logging test metrics...")
    from random import randint
    
    for day in range(7):
        dm.log_metrics(
            experiment_id=exp_id,
            variant_name='control',
            date_val=date.today(),
            impressions=1000,
            conversions=randint(80, 120),
            revenue=randint(800, 1200)
        )
        
        dm.log_metrics(
            experiment_id=exp_id,
            variant_name='variant_a',
            date_val=date.today(),
            impressions=1000,
            conversions=randint(100, 140),
            revenue=randint(1000, 1400)
        )
    
    print("✅ Logged metrics\n")
    
    # Get results
    print("Fetching results...")
    results = dm.get_experiment_results(exp_id)
    print("\n📊 Results:")
    print(results)
    
    print("\n✅ Data manager is working!")