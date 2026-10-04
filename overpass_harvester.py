import csv
import json
import requests
from transaction_logger import log_system_event

def harvest_malawi_urban_hubs():
    print("\n=======================================================")
    print("🛰️  MALAWI URBAN HUBS MASS INGESTION ENGINE 🛰️")
    print("=======================================================\n")
    
    # We lock directly on the verified active operational mirror server
    overpass_url = "https://kumi.systems"
    
    headers = {
        "User-Agent": "MalawiAddressingSystemInfrastructure/3.0 (contact: core_dev@domain.mw)",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    target_cities = [
        ("Lilongwe", -13.9626, 33.7741, 15000),
        ("Blantyre", -15.7861, 35.0058, 15000),
        ("Zomba", -15.3875, 35.3181, 10000),
        ("Mzuzu", -11.4584, 34.0151, 10000)
    ]
    
    csv_filename = "government_plots.csv"
    total_saved = 0
    
    log_system_event("OVERPASS_RUN", f"Targeting verified active spatial gateway: {overpass_url}")
    
    for city, lat, lon, radius in target_cities:
        print(f"\n🚀 [PIPELINE] Sweeping target urban zones for: {city}...")
        
        # Fixed explicit query structure string layout format
        city_query = f'[out:json][timeout:45];(node["amenity"~"hospital|clinic|school|marketplace"](around:{radius},{lat},{lon});node["leisure"="stadium"](around:{radius},{lat},{lon});node["shop"~"supermarket|convenience|clothes|hardware|mall"](around:{radius},{lat},{lon}););out body;'
        
        try:
            # We send raw data payloads via string conversion to maintain standard format parsing
            payload = f"data={city_query}"
            response = requests.post(overpass_url, data=payload, headers=headers, timeout=60)
            
            if response.status_code != 200:
                print(f"  └── ⚠️  Server status {response.status_code} returned for {city}. Advancing.")
                continue
                
            data = response.json()
            elements = data.get("elements", [])
            print(f"  └──  Success! Extracted {len(elements)} registered features for {city}.")
            
            saved_count = 0
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                for element in elements:
                    e_lat = element.get("lat")
                    e_lon = element.get("lon")
                    tags = element.get("tags", {})
                    name = tags.get("name", "").strip()
                    amenity = tags.get("amenity", tags.get("shop", tags.get("leisure", "LANDMARK"))).upper()
                    
                    if not name or not e_lat or not e_lon:
                        continue
                        
                    plot_code = f"OSM/{amenity[:3]}/{400 + total_saved + saved_count}"
                    zone_layer = f"{city} District - {name}"
                    
                    gate_desc = tags.get("operator", "Public / Commercial Registration")
                    wall_desc = f"Type: {amenity} | OSM ID: {element.get('id')}"
                    landmark_clue = f"Near coordinates: {e_lat}, {e_lon}"
                    
                    writer.writerow([plot_code, zone_layer, round(e_lat, 6), round(e_lon, 6), gate_desc, wall_desc, landmark_clue])
                    saved_count += 1
            
            print(f"  └── 📄 Appended {saved_count} clean nodes into '{csv_filename}'.")
            total_saved += saved_count
            log_system_event("OVERPASS_CITY_SUCCESS", f"Imported {saved_count} elements for {city}.")
            
        except Exception as error:
            print(f"  └── ❌ Parsing fail for {city}: {error}")
            
    print("\n" + "="*70)
    print("🏆 URBAN REGIONAL HARVEST COMPLETE")
    print(f"--> Combined Ingested Records Added to CSV : {total_saved} nodes.")
    print("="*70)
    if total_saved > 0:
        print("💡 Simply type: 'python batch_importer.py' to process and seed them offline!")

if __name__ == "__main__":
    harvest_malawi_urban_hubs()
