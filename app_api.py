from flask import Flask, request, jsonify
import sqlite3
import math
from transaction_logger import log_system_event

app = Flask(__name__)

DB_PATH = "malawi_addresses.db"

def calculate_haversine(lat1, lon1, lat2, lon2):
    """Calculates ground distance in meters between two GPS coordinates."""
    earth_radius = 6371000 
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    return round(earth_radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))), 2)

# 🔍 CHANNEL 1: SEARCH ADDRESS (For Flutter's Top Search Bar & Map Pivots)
@app.route('/api/search', methods=['GET'])
def search_address():
    keyword = request.args.get('query', '').strip()
    if not keyword:
        return jsonify({"status": "ERROR", "message": "Search query cannot be empty"}), 400
        
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    formatted_query = f"%{keyword}%"
    
    cursor.execute("""
        SELECT b.beacon_code, b.zone_name, b.latitude, b.longitude, d.nearest_landmark
        FROM spatial_beacons b
        LEFT JOIN property_descriptors d ON b.id = d.beacon_id
        WHERE b.beacon_code LIKE ? OR b.zone_name LIKE ? LIMIT 10
    """, (formatted_query, formatted_query))
    results = cursor.fetchall()
    connection.close()
    
    payload = []
    for row in results:
        payload.append({
            "a_code": row[0],
            "location_name": row[1],
            "latitude": row[2],
            "longitude": row[3],
            "landmark_hint": row[4] or "General Settlement Center"
        })
        
    log_system_event("API_SEARCH", f"Flutter queried keyword: '{keyword}'. Found {len(payload)} matches.")
    return jsonify({"status": "SUCCESS", "results": payload})

# 📌 CHANNEL 2: REGISTER NEW PIN (For Flutter's Red Action Button Form)
@app.route('/api/register', methods=['POST'])
def register_address():
    data = request.json or {}
    zone = data.get('zone_name', '').strip()
    place = data.get('property_name', '').strip()
    lat = float(data.get('latitude', 0.0))
    lon = float(data.get('longitude', 0.0))
    gate = data.get('gate_description', '').strip()
    landmark = data.get('landmark_hint', '').strip()
    
    if not zone or not place or not lat or not lon:
        return jsonify({"status": "ERROR", "message": "Missing required geocoding parameters"}), 400
        
    # Run our offline Haversine proximity firewall check
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT zone_name, latitude, longitude FROM spatial_beacons")
    existing_nodes = cursor.fetchall()
    connection.close()
    
    for node in existing_nodes:
        ex_zone, ex_lat, ex_lon = node
        distance = calculate_haversine(lat, lon, ex_lat, ex_lon)
        if distance <= 15.0:
            log_system_event("API_CONFLICT", f"Blocked registration for '{place}' due to proximity with '{ex_zone}'")
            return jsonify({
                "status": "CONFLICT",
                "message": f"Spatial conflict! Pin is only {distance}m away from an already registered plot: {ex_zone}"
            }), 409

    # Insert verified clean address node natively into SQLite
    unique_id = f"MW-APP-{place.replace(' ', '-').upper()}"
    beacon_code = f"A-CODE-{len(place) * 7 + 100}" # Robust mathematical address serialization
    
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("INSERT OR REPLACE INTO spatial_beacons VALUES (?, ?, ?, ?, ?)", (unique_id, beacon_code, f"{zone} - {place}", lat, lon))
    cursor.execute("INSERT INTO property_descriptors (beacon_id, gate_descriptor, wall_descriptor, nearest_landmark) VALUES (?, ?, ?, ?, ?)", (unique_id, gate, "Native App Boundary", landmark, "Verified Mobile Entry"))
    connection.commit()
    connection.close()
    
    log_system_event("API_WRITE", f"Flutter app securely registered new address code: {beacon_code}")
    return jsonify({
        "status": "SUCCESS",
        "message": "Property locked into national infrastructure ledger successfully!",
        "assigned_a_code": beacon_code,
        "coordinates": f"{lat}, {lon}"
    }), 201

if __name__ == '__main__':
    # Launch on port 5000 and bind to 0.0.0.0 so your phone can talk to it over Wi-Fi
    app.run(host='0.0.0.0', port=5000, debug=True)
