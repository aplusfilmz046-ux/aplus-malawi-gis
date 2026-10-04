import sqlite3
import math

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the absolute ground distance in meters between two sets of GPS degrees 
    using the spherical law of cosines / Haversine equation.
    """
    # Earth's radius in meters
    earth_radius = 6371000 
    
    # Convert decimal degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # Haversine core math formula execution
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance_meters = earth_radius * c
    return round(distance_meters, 2)

def validate_new_coordinate(new_lat, new_lon, threshold_meters=15.0):
    """
    Scans the local addressing database to ensure a newly submitted pin 
    is not overlapping an already registered physical structure.
    """
    connection = sqlite3.connect("malawi_addresses.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT id, beacon_code, zone_name, latitude, longitude FROM spatial_beacons")
    existing_nodes = cursor.fetchall()
    connection.close()
    
    print(f"\n🔍 [VALIDATOR] Auditing new target pin ({new_lat}, {new_lon}) against registry...")
    collision_detected = False
    
    for node in existing_nodes:
        node_id, code, zone, ex_lat, ex_lon = node
        
        # Calculate exactly how close the new point is to this existing database point
        gap_distance = calculate_haversine_distance(new_lat, new_lon, ex_lat, ex_lon)
        
        if gap_distance <= threshold_meters:
            print("\n⚠️  [SPATIAL COLLISION WARNING] ⚠️")
            print(f"--> The coordinates you entered are only {gap_distance} meters away from an existing address!")
            print(f"--> Overlapping Node ID : {node_id}")
            print(f"--> Registered Identity : {zone} ({code})")
            print("--> Action Required     : Please adjust your pin placement or verify the property plot.")
            collision_detected = True
            
    if not collision_detected:
        print("✅ [VALIDATOR PASS] Coordinates are clear! No overlapping properties found within 15 meters.")
        return True
    return False

if __name__ == "__main__":
    print("--- MALAWI GEOGRAPHIC PROXIMITY CHECKER ---")
    
    # Test 1: Testing a completely fresh, safe location far away from everything else
    validate_new_coordinate(-13.901111, 33.712222)
    print("=" * 75)
    
    # Test 2: Simulating a user making a mistake by dropping a pin right next to our Area 25 node (-13.8942, 33.7911)
    # We will pass a coordinate that is just a fraction of a degree off
    validate_new_coordinate(-13.894210, 33.791120)
