import os
import sqlite3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import tkinter as tk
from tkinter import ttk, messagebox

class APlusGISDesktopConsole:
    def __init__(self, root):
        self.root = root
        self.root.title("A+Malawi GIS Addressing Command Console v2.5")
        self.root.geometry("1200x670")
        self.root.configure(bg="#F4F6F8")
        
        # 📂 Local Relational Addressing SQLite Database Ledger Path Configuration
        self.db_path = r"D:\maping\malawi_addresses.db"
        self.initialize_database_tables()
        
        self.search_query = ""
        self.build_desktop_layout_tree()
        self.refresh_live_data_grid()
        
        # 📡 Spawn the live background over-the-air API receiver server gateway thread
        self.start_api_network_server()

    def initialize_database_tables(self):
        """Ensures the offline address registry tables exist safely on disk."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS address_nodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    property_name TEXT NOT NULL,
                    landmark_clues TEXT NOT NULL,
                    latitude TEXT NOT NULL,
                    longitude TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute("SELECT COUNT(*) FROM address_nodes")
            if cursor.fetchone()[0] == 0:
                mock_data = [
                    ("Sunrise Grocery Shop", "Opposite the water borehole pump station", "-13.9626", "33.7741"),
                    ("Area 49 Household Plot", "Near the community pharmacy brick wall", "-13.9540", "33.7810"),
                    ("Lilongwe Pentecostal Center", "Adjacent to the secondary school football field", "-13.9710", "33.7690")
                ]
                cursor.executemany("INSERT INTO address_nodes (property_name, landmark_clues, latitude, longitude) VALUES (?, ?, ?, ?)", mock_data)

    def build_desktop_layout_tree(self):
        """Draws the premium flag-branded multi-pane dashboard framework matrix."""
        # 🏢 LEFT NAVIGATION PANEL TOWER WING (Velvet Slate Black)
        sidebar = tk.Frame(self.root, bg="#0A0F0B", width=240)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        logo_label = tk.Label(sidebar, text="🇲🇼 A+MALAWI", bg="#0A0F0B", fg="#CE1126", font=("Arial", 16, "bold"))
        logo_label.pack(pady=(30, 2), anchor="w", padx=20)
        
        sub_logo = tk.Label(sidebar, text="GIS DESKTOP CONSOLE CORE", bg="#0A0F0B", fg="white", font=("Arial", 8, "bold"))
        sub_logo.pack(anchor="w", padx=22)
        
        lbl_status = tk.Label(sidebar, text="• STATION TERMINAL ACTIVE", bg="#0A0F0B", fg="#00E676", font=("Arial", 9, "bold"))
        lbl_status.pack(pady=40, anchor="w", padx=22)
        
        btn_delete = tk.Button(sidebar, text="❌ PURGE SELECTED NODE", bg="#CE1126", fg="white", font=("Arial", 10, "bold"), relief="flat", command=self.delete_selected_node)
        btn_delete.pack(side="bottom", fill="x", padx=15, pady=30)

        # 🖥️ RIGHT MAIN WORKSPACE CANVAS PANELS
        main_canvas = tk.Frame(self.root, bg="#F4F6F8")
        main_canvas.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        header_frame = tk.Frame(main_canvas, bg="#F4F6F8")
        header_frame.pack(fill="x", pady=(0, 12))
        
        header_title = tk.Label(header_frame, text="National Address Registry Node Control Tower", bg="#F4F6F8", fg="#0A0F0B", font=("Arial", 16, "bold"))
        header_title.pack(side="left", anchor="w")

        # 🔍 WIDESCREEN LIVE SEARCH FILTERS FRAME BAR
        search_frame = tk.Frame(header_frame, bg="#F4F6F8")
        search_frame.pack(side="right", anchor="e")
        
        search_lbl = tk.Label(search_frame, text="Search Ledger:", bg="#F4F6F8", fg="#0A0F0B", font=("Arial", 10, "bold"))
        search_lbl.pack(side="left", padx=(0, 6))
        
        self.search_entry = tk.Entry(search_frame, width=28, font=("Arial", 10))
        self.search_entry.pack(side="left", ipady=4, padx=(0, 6))
        self.search_entry.bind("<KeyRelease>", self.execute_live_search_filter)
        
        btn_search = tk.Button(search_frame, text="🔍 FILTER", bg="#008751", fg="white", font=("Arial", 9, "bold"), relief="flat", command=self.execute_live_search_filter)
        btn_search.pack(side="left", padx=(0, 4))
        
        btn_clear = tk.Button(search_frame, text="RESET", bg="grey", fg="white", font=("Arial", 9, "bold"), relief="flat", command=self.clear_search_filter)
        btn_clear.pack(side="left")
        
        # 📊 SERVER ANALYTICS TELEMETRY STRIP SHEET
        telemetry_strip = tk.Frame(main_canvas, bg="white", height=50, bd=1, relief="solid", highlightbackground="#E0E0E0")
        telemetry_strip.pack(fill="x", pady=(0, 16))
        telemetry_strip.pack_propagate(False)
        
        self.total_nodes_lbl = tk.Label(telemetry_strip, text="TOTAL MANAGED NODES: Counting...", bg="white", fg="#0A0F0B", font=("Arial", 11, "bold"))
        self.total_nodes_lbl.pack(side="left", padx=20, expand=True)
        
        self.filter_status_lbl = tk.Label(telemetry_strip, text="FILTER STATUS: Unfiltered Ledger", bg="white", fg="grey", font=("Arial", 10, "bold"))
        self.filter_status_lbl.pack(side="left", padx=20, expand=True)
        
        ping_lbl = tk.Label(telemetry_strip, text="GATEWAY: PORT 5000 ALIVE", bg="white", fg="#008751", font=("Arial", 10, "bold"))
        ping_lbl.pack(side="left", padx=20, expand=True)

        # 🗂️ CENTRAL SPREADSHEET LEDGER GRID VIEW
        grid_frame = tk.Frame(main_canvas, bg="white")
        grid_frame.pack(fill="both", expand=True)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), foreground="#0A0F0B")
        style.configure("Treeview", font=("Arial", 9), rowheight=26)
        
        self.data_grid = ttk.Treeview(grid_frame, columns=("ID", "Name", "Landmark Clues", "Latitude", "Longitude", "Source"), show="headings")
        
        self.data_grid.heading("ID", text="Index ID")
        self.data_grid.column("ID", width=70, anchor="center")
        self.data_grid.heading("Name", text="Property / Population Place Name")
        self.data_grid.column("Name", width=240, anchor="w")
        self.data_grid.heading("Landmark Clues", text="Visual Landmark Anchor Clues / Feature Type")
        self.data_grid.column("Landmark Clues", width=320, anchor="w")
        self.data_grid.heading("Latitude", text="Latitude")
        self.data_grid.column("Latitude", width=95, anchor="center")
        self.data_grid.heading("Longitude", text="Longitude")
        self.data_grid.column("Longitude", width=95, anchor="center")
        self.data_grid.heading("Source", text="Data Source")
        self.data_grid.column("Source", width=140, anchor="center")
        
        self.data_grid.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=self.data_grid.yview)
        self.data_grid.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def refresh_live_data_grid(self):
        """Universally scans and queries all tables and columns in the SQLite database dynamically."""
        for item in self.data_grid.get_children():
            self.data_grid.delete(item)
            
        search_token = self.search_query.strip()
        search_pattern = f"%{search_token}%"
        displayed_items_count = 0
        total_nodes_count = 0

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Fetch all tables present in the database file
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                tables = [row[0] for row in cursor.fetchall()]
                
                for table in tables:
                    cursor.execute(f"PRAGMA table_info([{table}]);")
                    table_info = cursor.fetchall()
                    col_names = [col[1] for col in table_info]
                    
                    if not col_names:
                        continue
                        
                    # Dynamically map best available columns for display
                    id_col = "rowid" if "rowid" in col_names else col_names[0]
                    name_col = next((c for c in ['property_name', 'name', 'key', 'title', 'place', 'area', 'location', 'address', 'Name', 'PLACE_NAME'] if c in col_names), col_names[1] if len(col_names) > 1 else col_names[0])
                    desc_col = next((c for c in ['landmark_clues', 'value', 'description', 'address', 'details', 'clues', 'DESCRIPTION', 'REMARKS'] if c in col_names), col_names[2] if len(col_names) > 2 else name_col)
                    lat_col = next((c for c in ['latitude', 'lat', 'LATITUDE', 'LAT'] if c in col_names), None)
                    lon_col = next((c for c in ['longitude', 'lon', 'lng', 'LONGITUDE', 'LON'] if c in col_names), None)
                    
                    select_id = id_col if id_col in col_names else f"rowid AS {id_col}"
                    select_name = name_col if name_col in col_names else "''"
                    select_desc = desc_col if desc_col in col_names else "''"
                    select_lat = lat_col if lat_col else "''"
                    select_lon = lon_col if lon_col else "''"
                    
                    # Query data based on search term filter presence
                    if search_token == "":
                        query = f"SELECT {select_id}, {select_name}, {select_desc}, {select_lat}, {select_lon} FROM [{table}] LIMIT 1000"
                        cursor.execute(query)
                    else:
                        # Universal multi-column search across all table columns
                        where_clauses = [f"CAST([{c}] AS TEXT) LIKE ?" for c in col_names]
                        query = f"SELECT {select_id}, {select_name}, {select_desc}, {select_lat}, {select_lon} FROM [{table}] WHERE " + " OR ".join(where_clauses)
                        params = tuple(search_pattern for _ in col_names)
                        cursor.execute(query, params)
                        
                    rows = cursor.fetchall()
                    source_label = f"📦 {table}"
                    
                    for row in rows:
                        rid = str(row[0]) if len(row) > 0 else ""
                        name_val = str(row[1]) if len(row) > 1 else ""
                        desc_val = str(row[2]) if len(row) > 2 else ""
                        lat_val = str(row[3]) if len(row) > 3 else ""
                        lon_val = str(row[4]) if len(row) > 4 else ""
                        
                        display_id = f"{table[:3].upper()}-{rid}"
                        self.data_grid.insert("", "end", values=(display_id, name_val, desc_val, lat_val, lon_val, source_label))
                        displayed_items_count += 1
                        total_nodes_count += 1

            # Update Telemetry Readouts
            self.total_nodes_lbl.config(text=f"TOTAL MANAGED NODES: {total_nodes_count}")
            if search_token:
                self.filter_status_lbl.config(text=f"FILTER STATUS: Showing {displayed_items_count} matches for '{search_token}'")
            else:
                self.filter_status_lbl.config(text="FILTER STATUS: Unfiltered Ledger")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to query database: {e}")

    def execute_live_search_filter(self, event=None):
        """Grabs text from the search entry box and refreshes grid view."""
        self.search_query = self.search_entry.get().strip()
        self.refresh_live_data_grid()

    def clear_search_filter(self):
        """Clears search input and resets ledger view."""
        self.search_entry.delete(0, tk.END)
        self.search_query = ""
        self.refresh_live_data_grid()

    def delete_selected_node(self):
        """Deletes the selected address node from the SQLite database."""
        selected_item = self.data_grid.selection()
        if not selected_item:
            messagebox.showwarning("Selection Warning", "Please select a node record from the ledger to purge.")
            return

        item_values = self.data_grid.item(selected_item, "values")
        if not item_values:
            return

        node_id_str = item_values[0]
        node_source = item_values[5]

        if "address_nodes" not in node_source:
            messagebox.showerror("Action Denied", "External sync dataset nodes are read-only and cannot be purged directly.")
            return

        actual_id = node_id_str.split("-")[-1]

        confirm = messagebox.askyesno("Confirm Purge", f"Are you sure you want to delete Node ID {actual_id}?")
        if confirm:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM address_nodes WHERE id = ?", (actual_id,))
                    conn.commit()
                messagebox.showinfo("Success", f"Node ID {actual_id} successfully purged.")
                self.refresh_live_data_grid()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Could not delete record: {e}")

    def start_api_network_server(self):
        """Starts a background HTTP server to receive location data over-the-air."""
        db_path_ref = self.db_path

        class GISAPIHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                try:
                    content_length = int(self.headers.get('Content-Length', 0))
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                    
                    prop_name = data.get('property_name', 'Unknown Location')
                    landmarks = data.get('landmark_clues', '')
                    lat = str(data.get('latitude', '0.0'))
                    lon = str(data.get('longitude', '0.0'))
                    
                    with sqlite3.connect(db_path_ref) as conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO address_nodes (property_name, landmark_clues, latitude, longitude) VALUES (?, ?, ?, ?)",
                            (prop_name, landmarks, lat, lon)
                        )
                        conn.commit()
                        
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "message": "Node recorded successfully"}).encode('utf-8'))
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                    
            def log_message(self, format, *args):
                return

        def run_server():
            try:
                server = HTTPServer(('0.0.0.0', 5000), GISAPIHandler)
                server.serve_forever()
            except Exception as e:
                print(f"API Server error: {e}")

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = APlusGISDesktopConsole(root)
    root.mainloop()