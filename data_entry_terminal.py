import sqlite3
from pyproj import Transformer

def convert_survey_to_wgs84(easting, northing):
    """Reuses our mathematical transformer engine from Step 5."""
    try:
        spatial_transformer = Transformer.from_crs("epsg:32736", "epsg:4326", always_xy=True)
        longitude, latitude = spatial_transformer.transform(easting, northing)
        return round(latitude, 6), round(longitude, 6)
    except Exception:
        return None

def interactive_data_entry():
    print("\n==============================================")
    print("🌟 MALAWI GLOBAL ADDRESS INGESTION TERMINAL 🌟")
    print("==============================================\n")
    
    # 1. Gather Location Classification
    print("Select Location Typology:")
    print(" [1] Formal Surveyed Plot (Has Concrete Beacon)")
    print(" [2] Informal/Public Point (No Physical Beacon - e.g., Shop, Bridge, House)")
    choice = input("Enter option (1 or 2): ").strip()
    
    zone_name = input("Enter general Area/Neighborhood (e.g., Area 25 C, Melody, Cape Maclear): ").strip()
    
    # 2. Handle Beacon vs Virtual Point Logic
    if choice == "1":
        beacon_code = input("Enter official stamp on concrete beacon (e.g., LL/49/150): ").strip()
        unique_id = f"LL-FORMAL-{beacon_code.replace('/', '-')}"
    else:
        poi_type = input("Enter type of place (e.g., Shop, House, Bridge, Church, Beach): ").strip().upper()
        poi_name = input("Enter the specific name or owner (e.g., Chinsapo Maize Mill, Joseph's House): ").strip()
        # Generate a unique virtual code based on location name length and type
        beacon_code = f"VIRTUAL-{poi_type}-{len(poi_name)}"
        unique_id = f"LL-VIRTUAL-{poi_type}-{hash(poi_name) % 10000}"
        zone_name = f"{zone_name} - {poi_name}"

    # 3. Gather Coordinates (Accepts standard GPS or Surveyor Grid Metrics)
    print("\nCoordinate Input Method:")
    print(" [A] Smartphone GPS (Decimal Latitude/Longitude)")
    print(" [B] Legal Layout Metrics (Easting X / Northing Y)")
    coord_choice = input("Enter choice (A or B): ").strip().upper()
    
    if coord_choice == "B":
        x = float(input("Enter Surveyor Easting (X): "))
        y = float(input("Enter Surveyor Northing (Y): "))
        lat, lon = convert_survey_to_wgs84(x, y)
    else:
        lat = float(input("Enter GPS Latitude (e.g., -13.9215): "))
        lon = float(input("Enter GPS Longitude (e.g., 33.7654): "))

    # 4. Gather Visual Descriptors (Our Critical Mapping Layer)
    print("\n🏠 Enter Property Visual Descriptors:")
    gate = input("Describe Gate (e.g., Black sliding gate, No gate): ").strip()
    wall = input("Describe Fence/Wall (e.g., Red brick, wire fence, green hedge): ").strip()
    landmark = input("Key Landmark Context Clue (e.g., Opposite the big mango tree, Near the borehole): ").strip()

    # 5. Commit Data to the Local Offline Database File
    connection = sqlite3.connect("malawi_addresses.db")
    cursor = connection.cursor()
    
    try:
        # Save to main node table
        cursor.execute("""
            INSERT OR REPLACE INTO spatial_beacons (id, beacon_code, zone_name, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
        """, (unique_id, beacon_code, zone_name, lat, lon))
        
        # Save to visual attributes table
        cursor.execute("""
            INSERT INTO property_descriptors (beacon_id, gate_descriptor, wall_descriptor, nearest_landmark)
            VALUES (?, ?, ?, ?)
        """, (unique_id, gate, wall, landmark))
        
        connection.commit()
        print("\n✅ SUCCESS: Location node permanently saved to database completely offline!")
        print(f"Generated Index Identifier: {unique_id}")
        print(f"Assigned Addressing Code: {beacon_code}")
        print(f"Locked Target Coordinates: {lat}, {lon}")
        
    except Exception as error:
        print(f"\n❌ Database error occurred: {error}")
    finally:
        connection.close()

if __name__ == "__main__":
    interactive_data_entry()
