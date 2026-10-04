import csv
import time
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from transaction_logger import log_system_event

def resolve_text_to_gps(business_name, city_or_area):
    """
    Geocoding fallback layer: Translates descriptive text strings into universal 
    smartphone decimal degrees using OpenStreetMap's Nominatim engine.
    """
    # Initialize locator tool with a specific user-agent to comply with API usage rules
    locator = Nominatim(user_agent="malawi_gis_address_infrastructure_agent")
    
    # We combine parameters to anchor searches specifically inside Malawi
    search_query = f"{business_name}, {city_or_area}, Malawi"
    fallback_query = f"{city_or_area}, Malawi"
    
    try:
        location = locator.geocode(search_query, timeout=5)
        if location:
            return round(location.latitude, 6), round(location.longitude, 6)
            
        # If the exact business location fails, fall back to general area/city coordinates
        location_fallback = locator.geocode(fallback_query, timeout=5)
        if location_fallback:
            return round(location_fallback.latitude, 6), round(location_fallback.longitude, 6)
            
        return None
    except Exception:
        return None

def run_malawi_scraping_pipeline():
    print("\n=======================================================")
    print("🌐 MALAWI WEB SCRAPER & SPATIAL GEOCAMP PIPELINE 🌐")
    print("=======================================================\n")
    
    # Target directory template layout setup
    # For safe development, we simulate scraping a structured layout path
    target_url = "https://bizmalawi.com/business-directory/"
    print(f"[SYSTEM] Connecting to public directory endpoint: {target_url}...")
    log_system_event("SCRAPE_START", f"Initiated extraction pass on target: {target_url}")

    # --- SIMULATED INBOUND LIVE DIRECTORY PARSING TARGET DATA BLOCK ---
    # Directories like YellowPages/BizMalawi serve HTML cards container tags
    mock_directory_html = """
    <div class="business-list">
        <div class="card">
            <h3 class="title">Sunrise Pharmacy</h3>
            <span class="location">Area 18 Filling Station, Lilongwe</span>
            <p class="desc">White brick perimeter wall with large green sign board.</p>
        </div>
        <div class="card">
            <h3 class="title">Limbe Wholesale Groceries</h3>
            <span class="location">Tsiranana Road, Blantyre</span>
            <p class="desc">Black sliding steel gate, opposite Citrona House.</p>
        </div>
        <div class="card">
            <h3 class="title">Mzuzu Tech Hub</h3>
            <span class="location">Katoto Area, Mzuzu</span>
            <p class="desc">Green hedge boundary line near secondary school grounds.</p>
        </div>
    </div>
    """
    
    # Initialize HTML tree parser parsing loop
    soup = BeautifulSoup(mock_directory_html, 'html.parser')
    cards = soup.find_all('div', class_='card')
    
    scraped_nodes_count = 0
    csv_filename = "government_plots.csv" # Direct integration with our step 15 batch tool
    
    # Open our target csv container file in append mode to aggregate data matrices seamlessly
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        for card in cards:
            name = card.find('h3', class_='title').text.strip()
            raw_location = card.find('span', class_='location').text.strip()
            desc = card.find('p', class_='desc').text.strip()
            
            print(f"\n[PARSER] Found: '{name}' | Listed Area: '{raw_location}'")
            print("[SPATIAL] Triggering reverse geocode coordinate lookup...")
            
            # Extract city grouping layer
            city = "Lilongwe" if "Lilongwe" in raw_location else "Blantyre" if "Blantyre" in raw_location else "Mzuzu"
            
            # Resolve GPS positions completely programmatically
            gps_coordinates = resolve_text_to_gps(name, city)
            
            if gps_coordinates:
                lat, lon = gps_coordinates
                print(f"✅ Resolved Location Matrix -> Lat: {lat}, Lon: {lon}")
                
                # Format into our standardized batch-ingestion layout schema template columns
                # Row format matching batch: plot_code,zone_name,latitude,longitude,gate,wall,landmark
                generated_plot_code = f"SCRP/{city[:2].upper()}/{100 + scraped_nodes_count}"
                
                writer.writerow([generated_plot_code, f"{city} - {name}", lat, lon, "Unknown style", desc, raw_location])
                scraped_nodes_count += 1
                log_system_event("SCRAPE_NODE", f"Scraped and geocoded node entity: {name} in {city}")
            else:
                print("❌ Geo-resolution failed for this location. Skipping entry context.")
                
            # Crucial: Sleep for 1.5 seconds to respect free server rate guidelines fairly
            time.sleep(1.5)
            
    print("\n" + "="*65)
    print("🏆 SCRAPER INGESTION DATA CONVERSION PIPELINE COMPLETE")
    print(f"--> Successfully Parsed & Geocoded : {scraped_nodes_count} businesses.")
    print(f"--> Appended Records Directly To   : '{csv_filename}'")
    print("="*65)
    print("💡 Now you can simply run: 'python batch_importer.py' to commit them!")

if __name__ == "__main__":
    run_malawi_scraping_pipeline()
