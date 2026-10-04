import sqlite3

def setup_address_database():
    # This connects to a local database file. If it doesn't exist, Python creates it.
    connection = sqlite3.connect("malawi_addresses.db")
    cursor = connection.cursor()

    print("[SYSTEM] Connected to local SQLite database engine...")

    # 1. Create the Master Spatial Beacons Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spatial_beacons (
            id TEXT PRIMARY KEY,
            beacon_code TEXT NOT NULL UNIQUE,
            zone_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    """)
    print("[SYSTEM] Table 'spatial_beacons' initialized successfully.")

    # 2. Create the Visual Property Descriptors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS property_descriptors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            beacon_id TEXT NOT NULL,
            gate_descriptor TEXT,
            wall_descriptor TEXT,
            nearest_landmark TEXT,
            FOREIGN KEY (beacon_id) REFERENCES spatial_beacons (id)
        )
    """)
    print("[SYSTEM] Table 'property_descriptors' initialized successfully.")

    # Commit structural changes and close out the connection safely
    connection.commit()
    connection.close()
    print("[SYSTEM] Database initialization complete! 'malawi_addresses.db' is ready.")

if __name__ == "__main__":
    setup_address_database()
