# 📌 CHANNEL 2: REGISTER NEW PIN (Matched to Flutter Frontend)
@app.route('/api/save_node', methods=['POST'])
def register_address():
    data = request.json or {}
    place = data.get('name', '').strip()
    landmark = data.get('landmark', '').strip()
    lat_str = data.get('latitude', '0.0')
    lon_str = data.get('longitude', '0.0')
    
    try:
        lat = float(lat_str)
        lon = float(lon_str)
    except ValueError:
        return jsonify({"status": "ERROR", "message": "Invalid coordinate format"}), 400
    
    if not place or lat == 0.0 or lon == 0.0:
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
    beacon_code = f"A-CODE-{len(place) * 7 + 100}" 
    
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO spatial_beacons (id, beacon_code, zone_name, latitude, longitude) VALUES (?, ?, ?, ?, ?)", 
        (unique_id, beacon_code, place, lat, lon)
    )
    # Fixed parameter binding count to match columns safely
    cursor.execute(
        "INSERT OR REPLACE INTO property_descriptors (beacon_id, gate_descriptor, wall_descriptor, nearest_landmark) VALUES (?, ?, ?, ?)", 
        (unique_id, "Mobile App Entry", "Native App Boundary", landmark)
    )
    connection.commit()
    connection.close()
    
    log_system_event("API_WRITE", f"Flutter app securely registered new address code: {beacon_code}")
    return jsonify({
        "status": "SUCCESS",
        "message": "Property locked into national infrastructure ledger successfully!",
        "assigned_a_code": beacon_code,
        "coordinates": f"{lat}, {lon}"
    }), 201