import sqlite3
import csv
import json

def export_address_infrastructure():
    # Establish read connection to our local database file
    connection = sqlite3.connect("malawi_addresses.db")
    cursor = connection.cursor()
    
    # SQL query joining physical mappings with our unique visual descriptors
    sql_query = """
        SELECT 
            b.id, 
            b.beacon_code, 
            b.zone_name, 
            b.latitude, 
            b.longitude, 
            d.gate_descriptor, 
            d.wall_descriptor, 
            d.nearest_landmark
        FROM spatial_beacons b
        LEFT JOIN property_descriptors d ON b.id = d.beacon_id
    """
    
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    connection.close()
    
    if not rows:
        print("❌ [EXPORTER] No address nodes found in the database to export.")
        return

    # --- FORMAT 1: EXPORT TO CSV (SPREADSHEET) ---
    csv_filename = "malawi_addresses_export.csv"
    headers = ["System_ID", "Beacon_Or_Virtual_Code", "Zone_Name", "Latitude", "Longitude", "Gate_Style", "Fence_Wall", "Landmark_Clue"]
    
    with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers) # Write table columns
        writer.writerows(rows)   # Write rows of addresses
        
    print(f"📄 [CSV EXPORTED] Created file: '{csv_filename}' (Perfect for Excel/Sheets)")

    # --- FORMAT 2: EXPORT TO STRUCTURED JSON (API DATA) ---
    json_filename = "malawi_addresses_api.json"
    json_dataset = []
    
    for row in rows:
        node = {
            "id": row[0],
            "address_code": row[1],
            "neighborhood": row[2],
            "coordinates": {
                "latitude": row[3],
                "longitude": row[4]
            },
            "visual_identifiers": {
                "gate": row[5],
                "wall_or_fence": row[6],
                "primary_landmark": row[7]
            }
        }
        json_dataset.append(node)
        
    with open(json_filename, "w", encoding="utf-8") as json_file:
        json.dump(json_dataset, json_file, indent=4, ensure_ascii=False)
        
    print(f"🌐 [JSON EXPORTED] Created file: '{json_filename}' (Ready for Taxi/Delivery App integration)")
    print("=" * 80)
    print("🚀 Extraction loop execution complete. Your addressing engine data is now portable!")

if __name__ == "__main__":
    print("--- MALAWI SPATIAL INFRASTRUCTURE DATA EXPORTER ---")
    export_address_infrastructure()
