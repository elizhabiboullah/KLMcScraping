import os

DB_FILE = "mcdonalds.db"

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Removed old database file: {DB_FILE}")
else:
    print("Database file not found. Nothing to remove.")
