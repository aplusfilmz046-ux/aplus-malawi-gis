import sqlite3

def offline_address_lookup(search_query):
    # Establish a fast local read connection
    connection = sqlite3.connect("malawi_addresses.db")
    cursor = connection.cursor()
    
    # We clean up the user text and add percentage wildcards for a true partial match search
    formatted_query = f"%{search_query.strip()}%"
    
    # This SQL query joins both tables together to pull physical and visual data simultaneously
    sql_command = """
        SELECT 
            b.beacon_code, 
            b.zone_name, 
            b.latitude, 
            b.longitude, 
            d.gate_descriptor, 
            d.wall_descriptor, 
            d.nearest_landmark
        FROM spatial_beacons b
        LEFT JOIN property_descriptors d ON b.id = d.beacon_id
        WHERE b.beacon_code LIKE ? OR b.zone_name LIKE ? OR d.nearest_landmark LIKE ?
    """
    
    cursor.execute(sql_command, (formatted_query, formatted_query, formatted_query))
    results = cursor.fetchall()
    connection.close()
    
    # Display the structured results back to the console
    if not results:
        print(f"\n❌ [SEARCH] No matching address coordinates found for: '{search_query}'")
        return
        
    print(f"\n🔍 [SEARCH] Found {len(results)} matching location node(s) for '{search_query}':")
    print("=" * 70)
    
    for row in results:
        beacon, zone, lat, lon, gate, wall, landmark = row
        print(f"📍 LOCATION: {zone} ({beacon})")
        print(f"🌐 COORDINATES: Latitude: {lat}, Longitude: {lon}")
        print(f"🏡 PROPERTY VISUALS:")
        print(f"   - Gate: {gate}")
        print(f"   - Fence/Wall: {wall}")
        print(f"   - Landmark Context: {landmark}")
        print("-" * 70)

if __name__ == "__main__":
    print("--- MALAWI DIGITAL ADDRESS RESOLUTION ENGINE TEST ---")
    
    # Test 1: Simulating typing a partial neighborhood name
    offline_address_lookup("Melody")
    
    # Test 2: Simulating typing a raw surveyor beacon serial stamp
    offline_address_lookup("25/102")
    
    # Test 3: Simulating typing a local landmark clue
    offline_address_lookup("clinic")
