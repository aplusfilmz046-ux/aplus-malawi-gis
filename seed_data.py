import sqlite3

def seed_initial_nodes():
    connection = sqlite3.connect("malawi_addresses.db")
    cursor = connection.cursor()

    # 1. Insert spatial beacon data (Simulating legal surveyor pins)
    beacons_to_add = [
        ("LL-A25-P102", "LL/25/102", "Area 25 Sector 2", -13.8942, 33.7911),
        ("LL-MELD-P42", "LL/49/M42", "Melody (Area 49)", -13.9215, 33.7654),
        ("LL-A18-P15",  "LL/18/015", "Area 18B",          -13.9581, 33.8102)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO spatial_beacons (id, beacon_code, zone_name, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    """, beacons_to_add)

    # 2. Insert corresponding visual identifier tokens
    descriptors_to_add = [
        ("LL-A25-P102", "Black sliding gate with spikes", "Red brick perimeter wall", "Opposite Chipiku Stores"),
        ("LL-MELD-P42", "Brown wooden double gate", "White concrete wall with razor wire", "Behind the Puma filling station"),
        ("LL-A18-P15",  "No gate, open driveway", "Green hedge fence line", "Near Area 18 health clinic intersection")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO property_descriptors (beacon_id, gate_descriptor, wall_descriptor, nearest_landmark)
        VALUES (?, ?, ?, ?)
    """, descriptors_to_add)

    connection.commit()
    connection.close()
    print("[SYSTEM] Sample Lilongwe addressing nodes successfully injected into the system database.")

if __name__ == "__main__":
    seed_initial_nodes()
