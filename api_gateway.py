from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os

# 1. Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection

DB_PATH = 'malawi_addresses.db'

print("--- MALAWI STANDALONE GIS API GATEWAY ONLINE ---")

# Serve the frontend landing page at the root URL
@app.route('/')
def serve_frontend():
    print("[API GATEWAY] Serving frontend landing page to client.")
    return send_from_directory('.', 'index.html')

# API status endpoint (moved to /api/status)
@app.route('/api/status', methods=['GET'])
def api_status():
    return jsonify({"status": "online", "message": "A+Malawi GIS API Gateway is active."})

@app.route('/api/addresses', methods=['GET'])
def get_addresses():
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM addresses')
        rows = cur.fetchall()
        con.close()
        return jsonify([dict(row) for row in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/register', methods=['POST'])
def register_address():
    data = request.json
    try:
        address_code = f"MW-{data.get('region', 'LL').upper()}-{int(float(data.get('lat', 0))*1000)}"
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute('''
            INSERT INTO addresses (address_code, full_name, phone, address_type, latitude, longitude, region)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (address_code, data.get('fullName'), data.get('phone'), data.get('addressType'), data.get('lat'), data.get('lng'), data.get('region')))
        con.commit()
        con.close()
        print(f"[HTTP RESPONSE] Successfully registered address code: {address_code}")
        return jsonify({"success": True, "addressCode": address_code})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)