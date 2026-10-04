import csv
import time
from geopy.geocoders import Nominatim
from transaction_logger import log_system_event

def harvest_national_features():
    print("\n=======================================================")
    print("🌍 MALAWI NATIONAL GEOGRAPHIC LANDMARK HARVESTER 🌍")
    print("=======================================================\n")
    print("[SYSTEM] Compiling prominent Malawian geographical nodes...")
    
    # 1. Structured National Features Dataset grouped by typology category
    national_registry = [
        # --- RIVERS & LAKES ---
        {"name": "Lake Malawi", "type": "LAKE", "zone": "Mangochi / Nkhata Bay", "landmark": "Main water body of Malawi"},
        {"name": "Shire River", "type": "RIVER", "zone": "Chikwawa / Nsanje", "landmark": "Major outflow connecting to Zambezi"},
        {"name": "Lake Chilwa", "type": "LAKE", "zone": "Zomba", "landmark": "Endorheic lake on eastern border"},
        
        # --- GAME RESERVES & NATIONAL PARKS ---
        {"name": "Liwonde National Park", "type": "GAME_RESERVE", "zone": "Machinga", "landmark": "Protected wildlife conservation area"},
        {"name": "Majete Wildlife Reserve", "type": "GAME_RESERVE", "zone": "Chikwawa", "landmark": "Big five wildlife tracking center"},
        {"name": "Kasungu National Park", "type": "GAME_RESERVE", "zone": "Kasungu", "landmark": "Central region wilderness reserve"},
        {"name": "Nyika National Park", "type": "GAME_RESERVE", "zone": "Rumphi", "landmark": "Montane plateau wildlife reserve"},
        
        # --- MOUNTAINS & PLATEAUS ---
        {"name": "Mulanje Mountain", "type": "MOUNTAIN", "zone": "Mulanje", "landmark": "Sapitwa Peak - Highest point in Malawi"},
        {"name": "Zomba Plateau", "type": "MOUNTAIN", "zone": "Zomba", "landmark": "Forest highland plateau overlook"},
        {"name": "Dedza Mountain", "type": "MOUNTAIN", "zone": "Dedza", "landmark": "High altitude central region peak"},
        
        # --- FOREST RESERVES ---
        {"name": "Dzalanyama Forest Reserve", "type": "FOREST", "zone": "Lilongwe / Dedza", "landmark": "Critical water catchment forest"},
        {"name": "Viphya Forest", "type": "FOREST", "zone": "Mzimba", "landmark": "Chikangawa massive pine plantation"},
        
        # --- TRADING CENTERS & MAJOR HUBS ---
        {"name": "Zalewa Trading Center", "type": "TRADING_CENTER", "zone": "Neno", "landmark": "Major highway junction checkpoint"},
        {"name": "Limbe Market", "type": "TRADING_CENTER", "zone": "Blantyre", "landmark": "Primary commercial trading center"},
        {"name": "Jenda Trading Center", "type": "TRADING_CENTER", "zone": "Mzimba", "landmark": "Border town junction point"},
        
        # --- HOSPITALS & SCHOOLS ---
        {"name": "Kamuzu Central Hospital", "type": "HOSPITAL", "zone": "Lilongwe City Center", "landmark": "Main referral clinic hub"},
        {"name": "Queen Elizabeth Central Hospital", "type": "HOSPITAL", "zone": "Blantyre", "landmark": "Southern region referral hub"},
        {"name": "University of Malawi UNIMA", "type": "SCHOOL", "zone": "Zomba", "landmark": "Main campus institutional grounds"}
    ]

    # Initialize geolocator client with structured header constraints
    locator = Nominatim(user_agent="malawi_national_gis_harvester_daemon")
    
    csv_filename = "government_plots.csv"
    successful_harvests = 0
    
    print(f"[SYSTEM] Opening data pipeline channel: '{csv_filename}'")
    log_system_event("HARVEST_START", f"Starting national geographical harvest for {len(national_registry)} targets.")
    
    # Open file in append mode to add data smoothly without deleting your existing plot rows
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        for index, item in enumerate(national_registry, start=1):
            name = item["name"]
            category = item["type"]
            zone = item["zone"]
            landmark_clue = item["landmark"]
            
            print(f"\n[NODE {index}/{len(national_registry)}] Harvesting: {name} ({category})")
            
            # Formulate structured geographic query parameters centered on Malawi
            search_query = f"{name}, Malawi"
            
            try:
                location = locator.geocode(search_query, timeout=6)
                if location:
                    lat = round(location.latitude, 6)
                    lon = round(location.longitude, 6)
                    print(f"  └── 📍 GPS Located: {lat}, {lon}")
                    
                    # Generate standardized custom plot identifiers matching our system schema parameters
                    generated_plot_code = f"NAT/{category[:3]}/{200 + index}"
                    formatted_zone_name = f"{zone} - {name}"
                    
                    # Row format: plot_code,zone_name,latitude,longitude,gate,wall,landmark
                    writer.writerow([
                        generated_plot_code, 
                        formatted_zone_name, 
                        lat, 
                        lon, 
                        "Natural Feature / Public Ground", 
                        f"Category: {category}", 
                        landmark_clue
                    ])
                    
                    successful_harvests += 1
                    log_system_event("HARVEST_SUCCESS", f"Committed national geographic feature: {name}")
                else:
                    print("  └── ❌ Location not resolved by free spatial mapping nodes.")
                    log_system_event("HARVEST_MISS", f"Could not find coordinates for: {name}")
                    
            except Exception as error:
                print(f"  └── ❌ API connection timeout/error: {error}")
                
            # Crucial: Sleep 1.5 seconds to respect free usage fair-use query guidelines nicely
            time.sleep(1.5)
            
    print("\n" + "="*65)
    print("🏆 NATIONAL GEOGRAPHIC HARVEST TRANSACTION COMPLETE")
    print(f"--> Successfully Geocoded & Ingested : {successful_harvests} national nodes.")
    print(f"--> Data Appended Safely To          : '{csv_filename}'")
    print("="*65)
    print("💡 Next step: Run 'python batch_importer.py' to pipe them to your database!")

if __name__ == "__main__":
    harvest_national_features()
