from tinydb import TinyDB, Query
from datetime import datetime

# Create or open the TinyDB JSON file
db = TinyDB("sports_tracker_data.json")


def initialize_tables():
    # Touch the tables to ensure they exist
    db.table("parlays")
    db.table("live_scores")
    db.table("rosters")
    db.table("users")
    db.table("meta")


def insert_sample_data():
    # Insert default parlay
    db.table("parlays").insert(
        {
            "user_id": "init_user",
            "wager": 25,
            "odds": 8,
            "status": "pending",
            "legs": [],
            "created_at": datetime.utcnow().isoformat(),
        }
    )

    # Insert a DB version
    db.table("meta").upsert(
        {"key": "db_version", "version": 1}, Query().key == "db_version"
    )


if __name__ == "__main__":
    initialize_tables()
    insert_sample_data()
    print("✅ TinyDB initialized with sample data.")
