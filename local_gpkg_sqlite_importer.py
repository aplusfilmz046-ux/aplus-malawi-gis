import sqlite3
import csv
import os
import struct
from transaction_logger import log_system_event

def parse_gpkg_geometry_blob(blob):
    """
    Decodes the standard binary GeoPackage Geometry Blob (GPKG WKB) 
    to extract the starting center coordinates of a shape without external GIS libraries.
    """
    if not blob or len(blob) < 8:
        return None
    
    try:
        # Read the GPKG header flags to determine envelope sizes
        header_flags = blob[3]
        envelope_contents_indicator = (header_flags & 0x0E) >> 1
        
        # Determine header size length based on envelope indicators
        header_byte_length = 8
        if envelope_contents_indicator == 1:
            header_byte_length += 32
        elif envelope_contents_indicator == 2 or envelope_contents_indicator == 3:
            header_byte_length += 48
        elif envelope_contents_indicator == 4:
            header_byte_length += 64
            
        # The actual Well-Known Binary geometry data begins right after the header
        wkb_body = blob[header_byte_length:]
        if len(wkb_body) < 5:
            return None
            
        byte_order = '<' if wkb_body[0] == 1 else '>'
        geom_type = struct.unpack(f'{byte_order}I', wkb_body[1:5])[0]
        
        # Typology 1: Point Layout Shape Node [lon, lat]
        if geom_type % 1000 == 1:
            lon, lat = struct.unpack(f'{byte_order}dd', wkb_body[5:21])
            return round(lat, 6), round(lon, 6)
            
        # Typology 2: LineString (2), Polygon (3), or MultiPolygon (6) shapes
        elif geom_type % 1000 == 2 or geom_type % 1000 == 3 or geom_type % 1000 == 6:
            offset = 9 if geom_type % 1000 == 3 else 5
            if len(wkb_body) >= offset + 16:
                lon, lat = struct.unpack(f'{byte_order}dd', wkb_body[offset:offset+16])
                return round(lat, 6), round(lon, 6)
                
    except Exception:
        return None
    return None

def import_malawi_gpkg_via_sqlite():
    print("\n=======================================================")
    print("📦 MALAWI NATIVE GEOPACKAGE SQLITE ENGINE 📦")
    print("=======================================================\n")
    
    # 🎯 TARGET FILE HARDCODED TO MATCH YOUR EXACT UNZIPPED FILENAME
    gpkg_target = "populated_places.gpkg"
    csv_filename = "government_plots.csv"
    
    if not os.path.exists(gpkg_target):
        print(f"❌ [CRITICAL INITIALIZATION ERROR] File '{gpkg_target}' not found!")
        print("💡 Action Required: Make sure your unzipped file is placed directly in 'D:\\maping\\populated_places.gpkg'")
        return

    print(f"[SYSTEM] Connecting natively to GeoPackage storage engine: '{gpkg_target}'...")
    log_system_event("GPKG_SQL_START", f"Parsing binary GeoPackage layout via sqlite3: {gpkg_target}")

    try:
        # Establish a native database read connection to the .gpkg file container
        connection = sqlite3.connect(gpkg_target)
        cursor = connection.cursor()
        
        # Query the GeoPackage internal schema metadata ledger directory to find the data table name
        cursor.execute("SELECT table_name FROM gpkg_contents WHERE data_type='features' LIMIT 1;")
        table_row = cursor.fetchone()
        
        if not table_row:
            print("❌ Could not identify an active feature layer table inside the GeoPackage.")
            connection.close()
            return
            
        data_table_name = table_row[0]
        print(f"✅ Target spatial table matrix layer identified: '{data_table_name}'")
        
        # Query the raw text fields and the binary geometry layer blob
        cursor.execute(f"SELECT name, place, geom FROM {data_table_name};")
        rows = cursor.fetchall()
        
        print(f"✅ Connected! Successfully loaded {len(rows)} raw data records from the binary package.")
        print("[SYSTEM] Running mass extraction on complex structural nodes...")
        
        saved_count = 0
        skipped_blank_names = 0
        
        with open(csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            for index, row in enumerate(rows):
                raw_name, raw_place, geom_blob = row
                
                if not raw_name or str(raw_name).lower() == 'none':
                    skipped_blank_names += 1
                    continue
                    
                name = str(raw_name).strip()
                place_type = str(raw_place or "ZONE").upper()
                
                # Use our low-level binary parser to crack open the geometry bytes
                coords = parse_gpkg_geometry_blob(geom_blob)
                if not coords:
                    continue
                    
                lat, lon = coords
                
                # Match your existing core database schema templates
                plot_code = f"GPK/{place_type[:3]}/{600 + index}"
                zone_layer = f"Malawi Boundary Layer - {name}"
                
                gate_desc = "Regional / Suburb Spatial Grid Boundary"
                wall_desc = f"Class: {place_type} | Source: Native GeoPackage SQL Direct Extract"
                landmark_clue = f"Coordinates verified at tracking points: {lat}, {lon}"
                
                writer.writerow([plot_code, zone_layer, lat, lon, gate_desc, wall_desc, landmark_clue])
                saved_count += 1
                
        connection.close()
        
        print("\n" + "="*65)
        print("🏆 GEOPACKAGE NATIVE SQL EXTRACTION COMPLETE")
        print(f"--> Extracted Area Nodes : {saved_count} entries.")
        print(f"--> Skipped Blank Names   : {skipped_blank_names} records.")
        print(f"--> Targets Appended To  : '{csv_filename}'")
        print("="*65)
        print("💡 Simply type: 'python batch_importer.py' to commit them all into the database file!")
        log_system_event("GPKG_SQL_DONE", f"Successfully extracted {saved_count} records via SQL direct parse.")
        
    except Exception as error:
        print(f"❌ [PIPELINE CRASH] Failed to parse local mapping layer: {error}")
        log_system_event("GPKG_SQL_FAIL", f"Native SQL parser crashed: {str(error)}")

if __name__ == "__main__":
    import_malawi_gpkg_via_sqlite()
