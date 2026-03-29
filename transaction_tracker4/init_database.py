import sqlite3
import os

# Import your dynamic schema directly from your main app!
# This guarantees the database and the UI will NEVER fall out of sync.
from app import ALL_FIELDS, DB_FILE

def build_dynamic_vault():
    """Reads the schema from app.py and forges the SQLite table."""
    if os.path.exists(DB_FILE):
        print(f"⚠️ Vault already exists at {DB_FILE}.")
        print("Delete the old .db file and run this again to rebuild.")
        return
        
    print(f"🛡️ Forging Dynamic Database Vault at: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # We always include a primary key and creation timestamp
    columns_sql = ["Record_ID TEXT PRIMARY KEY", "Created_At TEXT"]
    
    # Add all 46 user-defined fields from your app.py matrix as TEXT
    for field in ALL_FIELDS:
        columns_sql.append(f"{field} TEXT")
        
    # Create the exact table name that Pandas is looking for
    create_table_command = f"CREATE TABLE dynamic_ledger ({', '.join(columns_sql)})"
    
    try:
        cursor.execute(create_table_command)
        conn.commit()
        print("✅ Vault Provisioned Successfully. The Meta-Architecture is locked.")
    except sqlite3.Error as e:
        print(f"❌ Database creation failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    build_dynamic_vault()