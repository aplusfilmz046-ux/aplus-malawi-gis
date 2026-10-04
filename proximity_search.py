import sqlite3
import math
from transaction_logger import log_system_event

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """Calculates ground distance in meters between two sets of GPS degrees."""
    earth_radius = 6371000 
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(earth_radius * c, 2)

def find_closest_addresses(user_lat, user_lon, max_results=3):
    """
    Scans the database completely offline, calculates proximity, 
    and sorts the top closest physical structures near the user coordinates.
    """
    connection = sqlite3.connect("malawi_addresses.db")
    cursor = connection.cursor()
    
    # Fetch all registered points and join their visual navigation details
    sql_command = """
        SELECT 
            b.beacon_code, b.zone_name, b.latitude, b.longitude, 
            d.gate_descriptor, d.nearest_landmark
        FROM spatial_beacons b
        LEFT JOIN property_descriptors d ON b.id = d.beacon_id
    """
    cursor.execute(sql_command)
    all_nodes = cursor.fetchall()
    connection.close()
    
    scored_results = []
    
    # Calculate distance for every single registered address node
    for node in all_nodes:
        code, zone, target_lat, target_lon, gate, landmark = node
        distance = calculate_haversine_distance(user_lat, user_lon, target_lat, target_lon)
        
        scored_results.append({
            "code": code,
            "zone": zone,
            "distance": distance,
            "gate": gate,
            "landmark": landmark
        })
        
    # Sort the addresses based on distance (closest first)
    scored_results.sort(key=lambda x: x["distance"])
    
    # Trim to our target maximum results count
    top_matches = scored_results[:max_results]
    
    print(f"\n📡 [PROXIMITY RADAR] Scanning infrastructure nodes near: ({user_lat}, {user_lon})")
    print("=" * 80)
    print(f"{'DISTANCE':<12} | {'ADDRESS CODE':<15} | {'ZONE & NEIGHBORHOOD LAYER'}")
    print("=" * 80)
    
    for match in top_matches:
        print(f"{str(match['distance']) + ' meters':<12} | {match['code']:<15} | {match['zone']}")
        print(f"             ↳ 🏡 Visual Context: Gate: {match['gate']} | Near: {match['landmark']}")
        print("-" * 80)
        
    log_system_event("RADAR_SEARCH", f"Executed reverse GPS proximity scan near coordinate pair ({user_lat}, {user_lon}).")
    return top_matches

if __name__ == "__main__":
    print("--- MALAWI GEOGRAPHIC PROXIMITY SEARCH SCANNER ---")
    
    # Let's mock simulate a passenger standing right inside Melody Area 49 
    # trying to fetch the closest registered physical markers near them
    mock_passenger_latitude = -13.921600
    mock_passenger_longitude = 33.765500
    
    find_closest_addresses(mock_passenger_latitude, mock_passenger_longitude)
