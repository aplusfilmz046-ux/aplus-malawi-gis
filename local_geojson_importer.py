import json
import csv
import os
from transaction_logger import log_system_event

def extract_flat_coordinates(geometry):
    """
    Safeguards the data ingest pipeline against mixed-geometry layers.
    Flattens multi-point or polygon array list matrix layouts down to a flat coordinate pair.
    """
    if not geometry:
        return None
        
    g_type = geometry.get("type", "").upper()
    coords = geometry.get("coordinates", [])
    
    if not coords:
        return None
        
    try:
        # Typology Category 1: Standard flat point node pair [longitude, latitude]
        if g_type == "POINT" and not isinstance(coords[0], list):
            return float(coords[0]), float(coords[1])
            
        # Typology Category 2: MultiPoint or simple single LineString structure array matrix
        elif isinstance(coords[0], list) and not isinstance(coords[0][0], list):
            return float(coords[0][0]), float(coords[0][1])
            
        # Typology Category 3: Complex Polygon or MultiPolygon nested structural layers matrix
        elif isinstance(coords[0], list) and isinstance(coords[0][0], list):
            # Dive directly to the absolute innermost node coordinates pair layer
            inner_node = coords[0][0]
            while isinstance(inner_node, list) and len(inner_node) > 0:
                if not isinstance(inner_node[0], list):
                    break
                inner_node = inner_node[0]
            return float(inner_node[0]), float(inner_node[1])
            
    except (IndexError, ValueError, TypeError):
        return None
        
    return None

def import_malawi_geojson_data():
    print("\n=======================================================")
    print("📦 MALAWI LOCAL GEOJSON INGESTION PIPELINE 📦")
    print("=======================================================\n")
    
    # 🎯 TARGET FILE CONFIGURATION
    geojson_target = "populated_places.geojson"
    csv_filename = "government_plots.csv"
    
    if not os.path.exists(geojson_target):
        print(f"❌ [CRITICAL INITIALIZATION ERROR] File '{geojson_target}' not found!")
        return

    print(f"[SYSTEM] Opening local national dataset file: '{geojson_target}'...")
    log_system_event("GEOJSON_START", f"Opening offline dataset file: {geojson_target}")

    try:
        # Open and load the GeoJSON file using Python's native json module
        with open(geojson_target, "r", encoding="utf-8") as file:
            geojson_data = json.load(file)
            
        features = geojson_data.get("features", [])
        print(f"✅ Success! Loaded {len(features)} raw geographic records completely offline.")
        print("[SYSTEM] Compiling rows and mapping coordinates...")
        
        saved_count = 0
        skipped_blank_names = 0
        skipped_bad_geometry = 0
        
        # Open your central spreadsheet pipeline template in append mode
        with open(csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            for index, feature in enumerate(features):
                properties = feature.get("properties", {}) or {}
                geometry = feature.get("geometry", {}) or {}
                
                # Safe Extraction Layer: Skip if name field is missing
                raw_name = properties.get("name")
                if raw_name is None:
                    skipped_blank_names += 1
                    continue
                    
                name = str(raw_name).strip()
                if not name: 
                    skipped_blank_names += 1
                    continue
                    
                place_type = str(properties.get("place", "LANDMARK")).upper()
                
                # Use our newly added robust flattening function block to resolve numbers safely
                resolved_coords = extract_flat_coordinates(geometry)
                
                if not resolved_coords:
                    skipped_bad_geometry += 1
                    continue
                    
                lon, lat = resolved_coords
                
                # Match your existing core database schema templates
                plot_code = f"GEO/{place_type[:3]}/{500 + index}"
                zone_layer = f"Malawi Territory - {name}"
                
                gate_desc = "Public Ground / Settlement Center"
                wall_desc = f"Typology Class: {place_type} | Data Source: OSM Offline GeoJSON Pack"
                landmark_clue = f"Offline localized grid node points: {round(lat, 6)}, {round(lon, 6)}"
                
                # Append row data to your central csv pipeline template
                writer.writerow([plot_code, zone_layer, round(lat, 6), round(lon, 6), gate_desc, wall_desc, landmark_clue])
                saved_count += 1
                
        print("\n" + "="*65)
        print("🏆 LOCAL OFFLINE DATA SEGMENTATION COMPLETE")
        print(f"--> Extracted & Structured Nodes : {saved_count} entries.")
        print(f"--> Skipped Blank/Unnamed Fields : {skipped_blank_names} records.")
        print(f"--> Skipped Bad/Complex Shapes   : {skipped_bad_geometry} records.")
        print(f"--> Combined Targets Appended To : '{csv_filename}'")
        print("="*65)
        print("💡 Simply type: 'python batch_importer.py' to commit them all into the database file!")
        log_system_event("GEOJSON_DONE", f"Successfully extracted {saved_count} records. Skipped {skipped_blank_names} blank entries.")
        
    except Exception as error:
        print(f"❌ [PIPELINE CRASH] Failed to parse local mapping layer: {error}")
        log_system_event("GEOJSON_FAIL", f"Local parser crashed: {str(error)}")

if __name__ == "__main__":
    import_malawi_geojson_data()
