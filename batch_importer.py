import sqlite3
import csv
from transaction_logger import log_system_event
from secure_terminal import check_for_collisions

def run_bulk_ingestion_pipeline(csv_file_path):
    print("\n=======================================================")
    print("🚀 MALAWI BATCH SPATIAL IMPORT PIPELINE ACTIVE 🚀")
    print("=======================================================\n")
    print(f"[SYSTEM] Opening bulk survey spreadsheet: '{csv_file_path}'")
    
    connection = sqlite3.connect("malawi_addresses.db")
    cursor = connection.cursor()
    
    successful_writes = 0
    skipped_writes = 0
    
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for index, row in enumerate(csv_reader, start=1):
                code = row["plot_code"].strip()
                zone = row["zone_name"].strip()
                lat = float(row["latitude"])
                lon = float(row["longitude"])
                gate = row["gate"].strip()
                wall = row["wall"].strip()
                landmark = row["landmark"].strip()
                
                print(f"\n[ROW {index}] Checking constraints for plot: {code} ({zone})...")
                
                # Check if this spreadsheet point conflicts with existing data in our system
                audit = check_for_collisions(lat, lon)
                
                if audit["status"] == "CONFLICT":
                    print(f"⚠️  [BULK SKIP] Coordinate overlap detected! Skipped plot {code}. Only {audit['distance']}m from {audit['zone']}.")
                    log_system_event("BATCH_SKIP", f"Skipped bulk plot {code} due to spatial conflict with {audit['zone']}.")
                    skipped_writes += 1
                    continue
                
                # If safe, write it to the database file
                unique_id = f"LL-BULK-{code.replace('/', '-')}"
                
                cursor.execute("""
                    INSERT OR REPLACE INTO spatial_beacons (id, beacon_code, zone_name, latitude, longitude)
                    VALUES (?, ?, ?, ?, ?)
                """, (unique_id, code, zone, lat, lon))
                
                cursor.execute("""
                    INSERT INTO property_descriptors (beacon_id, gate_descriptor, wall_descriptor, nearest_landmark)
                    VALUES (?, ?, ?, ?)
                """, (unique_id, gate, wall, landmark))
                
                successful_writes += 1
                log_system_event("BATCH_WRITE", f"Successfully imported bulk land plot node: {code} ({zone})")
                
        # Commit the transaction block safely
        connection.commit()
        print("\n" + "="*60)
        print("✅ BULK PIPELINE PROCESSING LOOP COMPLETE")
        print(f"--> Successfully Ingested : {successful_writes} new address nodes.")
        print(f"--> Skipped Overlaps       : {skipped_writes} records.")
        print("="*60)
        
    except Exception as error:
        print(f"❌ [CRITICAL SYSTEM FAILURE] Batch processing crashed: {error}")
        log_system_event("BATCH_CRASH", f"Pipeline failure: {str(error)}")
    finally:
        connection.close()

if __name__ == "__main__":
    run_bulk_ingestion_pipeline("government_plots.csv")
