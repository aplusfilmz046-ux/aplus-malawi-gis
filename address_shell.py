import sys
from search_engine import offline_address_lookup
from proximity_search import find_closest_addresses

def launch_addressing_system_shell():
    print("\n=======================================================")
    print("🌍 MALAWI GIS ADDRESS ENGINE INTERACTIVE SHELL 🌍")
    print("=======================================================")
    print("Type '1' to search by Keyword / Area Name / Beacon ID")
    print("Type '2' to search by Passenger GPS Coordinates")
    print("Type 'exit' or 'quit' to close the shell session")
    print("=======================================================\n")
    
    while True:
        try:
            user_input = input("A-Engine ➔ ").strip()
            
            # Exit conditions
            if user_input.lower() in ['exit', 'quit']:
                print("\n[SYSTEM] Terminating active addressing shell session. Goodbye!")
                sys.exit(0)
                
            if user_input == "1":
                keyword = input("Enter search text (e.g., Melody, Area 25, LL/18): ").strip()
                if keyword:
                    offline_address_lookup(keyword)
                else:
                    print("⚠️ Search text cannot be blank.")
                    
            elif user_input == "2":
                try:
                    lat = float(input("Enter Passenger Latitude (e.g., -13.9216): "))
                    lon = float(input("Enter Passenger Longitude (e.g., 33.7655): "))
                    find_closest_addresses(lat, lon)
                except ValueError:
                    print("❌ Invalid input! Coordinates must be numerical decimal values.")
                    
            else:
                print("❓ Unknown command. Type '1' for text search, '2' for GPS search, or 'exit' to quit.")
                
            print("\n" + "-"*65)
            
        except KeyboardInterrupt:
            print("\n\n[SYSTEM] Shell interrupted. Safely closing out.")
            break

if __name__ == "__main__":
    launch_addressing_system_shell()
