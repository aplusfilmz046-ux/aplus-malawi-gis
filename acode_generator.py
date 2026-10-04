import sqlite3
import hashlib

def generate_universal_acode(beacon_id, zone_abbreviation):
    """
    Generates a unique, clean, and highly human-readable 'A-Code' token
    by hashing the core beacon properties into a shortened suffix.
    """
    # 1. Create a deterministic short cryptographic string from the unique beacon_id
    hash_object = hashlib.md5(beacon_id.encode())
    short_hash = hash_object.hexdigest()[:4].upper() # Extract first 4 characters
    
    # 2. Structure into a clean, readable universal format
    # Format: LLW (Lilongwe) - ZONE - UNIQUE_TOKEN
    universal_acode = f"LLW-{zone_abbreviation.strip().upper()}-{short_hash}"
    return universal_acode

def register_and_print_acodes():
    connection = sqlite3.connect("malawi_addresses.db")
    cursor = connection.cursor()
    
    # Fetch our existing sample nodes from the database
    cursor.execute("SELECT id, zone_name, beacon_code FROM spatial_beacons")
    rows = cursor.fetchall()
    
    print("--- MALAWI UNIVERSAL A-CODE GENERATION MATRIX ---")
    print("=" * 75)
    print(f"{'ZONE REGISTRY':<25} | {'BEACON STAMP':<15} | {'GENERATED A-CODE':<20}")
    print("=" * 75)
    
    for row in rows:
        b_id, zone, code = row
        
        # Determine a quick zone abbreviation for the token structure
        if "25" in zone:
            zone_abbr = "A25"
        elif "Melody" in zone:
            zone_abbr = "MLD"
        elif "18" in zone:
            zone_abbr = "A18"
        else:
            zone_abbr = "GEN"
            
        # Generate the unique address token
        acode_token = generate_universal_acode(b_id, zone_abbr)
        print(f"{zone:<25} | {code:<15} | 🚀 {acode_token:<20}")
        
    print("=" * 75)
    print("💡 Users can now print these A-Codes on front walls or share them via SMS!")
    connection.close()

if __name__ == "__main__":
    register_and_print_acodes()
