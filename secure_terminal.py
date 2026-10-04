import sqlite3
import math
# Connect directly to our background auditing module
from transaction_logger import log_system_event

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """Calculates ground distance in meters between two GPS coordinates."""
    earth_radius = 6371000 
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi, delta_lambda = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    return round(earth_radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))), 2)

def check_for_collisions(new_lat, new_lon, threshold_meters=15.0):
    """Scans the master table data to find spatial overlap issues."""
    connection = sqlite3.connect("malawi_addresses.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, beacon_code, zone_name, latitude, longitude FROM spatial_beacons")
    existing_nodes = cursor.fetchall()
    connection.close()
    
    for node in existing_nodes:
        node_id, code, zone, ex_lat, ex_lon = node
        distance = calculate_haversine_distance(new_lat, new_lon, ex_lat, ex_lon)
        if distance <= threshold_meters:
            return {"status": "CONFLICT", "distance": distance, "zone": zone, "code": code}
    return {"status": "CLEAR"}

def secure_ingestion_loop():
    print("\n=======================================================")
    print("🔒 MALAWI SECURE INFRASTRUCTURE INGESTION TERMINAL 🔒")
    print("=======================================================\n")
    
    zone_name = input("Enter general Neighborhood/Area: ").strip()
    place_name = input("Enter specific name of property/shop: ").strip()
    lat = float(input("Enter GPS Latitude: "))
    lon = float(input("Enter GPS Longitude: "))
    
    print("\n[SYSTEM] Initiating real-time spatial validation loop...")
    audit_result = check_for_collisions(lat, lon)
    
    if audit_result["status"] == "CONFLICT":
        print("\n❌ [INGESTION REJECTED] ❌")
        
        # 📝 LIVE AUDIT RECORDING
        log_system_event("SECURITY_WARN", f"Rejected write for '{place_name}' due to spatial conflict with '{audit_result['zone']}' at distance {audit_result['distance']}m.")
        return

    print("✅ [SPATIAL AUDIT PASSED] No coordinate overlaps detected. Proceeding...")
    gate = input("\nDescribe Gate Style: ").strip()
    wall = input("Describe Boundary Wall/Fence: ").strip()
    landmark = input("Nearest Landmark Clue: ").strip()
    
    unique_id = f"LL-SECURE-{place_name.replace(' ', '-').upper()}"
    beacon_code = f"V-SECURE-{len(place_name)}"
    
    connection = sqlite3.connect("malawi_addresses.db")
    cursor = connection.cursor()
    cursor.execute("INSERT OR REPLACE INTO spatial_beacons VALUES (?, ?, ?, ?, ?)", (unique_id, beacon_code, f"{zone_name} - {place_name}", lat, lon))
    cursor.execute("INSERT INTO property_descriptors (beacon_id, gate_descriptor, wall_descriptor, nearest_landmark) VALUES (?, ?, ?, ?)", (unique_id, gate, wall, landmark))
    connection.commit()
    connection.close()
    
    # 📝 LIVE AUDIT RECORDING
    log_system_event("DB_WRITE", f"Permanently registered new structural address node code: {beacon_code} ({place_name})")
    print(f"\n🎉 [SUCCESS] Secure entry committed!")

if __name__ == "__main__":
    secure_ingestion_loop()
