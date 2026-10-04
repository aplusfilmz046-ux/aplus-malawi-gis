import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class APlusGISDesktopConsole:
    def __init__(self, root):
        self.root = root
        self.root.title("A+Malawi GIS Addressing Command Console v2.5")
        self.root.geometry("1180x670")
        self.root.configure(bg="#F4F6F8")
        
        # Connect and verify local database paths directly
        self.db_path = r"D:\maping\malawi_addresses.db"
        self.initialize_database_tables()
        
        self.search_query = ""
        self.build_desktop_layout_tree()
        self.refresh_live_data_grid()

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
        # LEFT NAVIGATION PANEL WING (Velvet Slate Black)
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

        # RIGHT MAIN WORKSPACE CANVAS PANELS
        main_canvas = tk.Frame(self.root, bg="#F4F6F8")
        main_canvas.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Top Header Row
        header_frame = tk.Frame(main_canvas, bg="#F4F6F8")
        header_frame.pack(fill="x", pady=(0, 12))
        
        header_title = tk.Label(header_frame, text="National Address Registry Node Control Tower", bg="#F4F6F8", fg="#0A0F0B", font=("Arial", 16, "bold"))
        header_title.pack(side="left", anchor="w")

        # WIDESCREEN LIVE SEARCH FILTERS FRAME BAR
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
        
        # SERVER ANALYTICS TELEMETRY STRIP SHEET
        telemetry_strip = tk.Frame(main_canvas, bg="white", height=50, bd=1, relief="solid", highlightbackground="#E0E0E0")
        telemetry_strip.pack(fill="x", pady=(0, 16))
        telemetry_strip.pack_propagate(False)
        
        self.total_nodes_lbl = tk.Label(telemetry_strip, text="TOTAL MANAGED NODES: Counting...", bg="white", fg="#0A0F0B", font=("Arial", 11, "bold"))
        self.total_nodes_lbl.pack(side="left", padx=20, expand=True)
        
        self.filter_status_lbl = tk.Label(telemetry_strip, text="FILTER STATUS: Unfiltered Ledger", bg="white", fg="grey", font=("Arial", 10, "bold"))
        self.filter_status_lbl.pack(side="left", padx=20, expand=True)
        
        ping_lbl = tk.Label(telemetry_strip, text="DATAFEED GATEWAY: ACTIVE", bg="white", fg="#008751", font=("Arial", 10, "bold"))
        ping_lbl.pack(side="left", padx=20, expand=True)

        # CENTRAL SPREADSHEET LEDGER GRID VIEW
        grid_frame = tk.Frame(main_canvas, bg="white")
        grid_frame.pack(fill="both", expand=True)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), foreground="#0A0F0B")
        style.configure("Treeview", font=("Arial", 9), rowheight=26)
        
        self.data_grid = ttk.Treeview(grid_frame, columns=("ID", "Name", "Landmark Clues", "Latitude", "Longitude", "Source"), show="headings")
        
        self.data_grid.heading("ID", text="Index ID")
        self.data_grid.column("ID", width=70, anchor="center")
        self.data_grid.heading("Name", text="Property / Population Place Name")
        self.data_grid.column("Name", width=220, anchor="w")
        self.data_grid.heading("Landmark Clues", text="Visual Landmark Anchor Clues / Spatial Boundaries")
        self.data_grid.column("Landmark Clues", width=340, anchor="w")
        self.data_grid.heading("Latitude", text="Latitude")
        self.data_grid.column("Latitude", width=90, anchor="center")
        self.data_grid.heading("Longitude", text="Longitude")
        self.data_grid.column("Longitude", width=90, anchor="center")
        self.data_grid.heading("Source", text="Data Source")
        self.data_grid.column("Source", width=140, anchor="center")
        
        self.data_grid.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=self.data_grid.yview)
        self.data_grid.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def refresh_live_data_grid(self):
        """Queries and filters database rows safely without nested loop blocks."""
        for item in self.data_grid.get_children():
            self.data_grid.delete(item)
            
        q = "%" + self.search_query.lower() + "%"
        displayed_items_count = 0
        user_nodes_count = 0
        bulk_nodes_count = 0

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Phase 1: Load live mobile address pins cleanly
            cursor.execute("SELECT id, property_name, landmark_clues, latitude, longitude FROM address_nodes WHERE LOWER(property_name) LIKE ? OR LOWER(landmark_clues) LIKE ?", (q, q))
            nodes = cursor.fetchall()
            for row in nodes:
                self.data_grid.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], "📱 Mobile Pin"))
                displayed_items_count += 1
                
            cursor.execute("SELECT COUNT(*) FROM address_nodes")
            user_nodes_count = cursor.fetchone()[0]

            # Phase 2: Load yesterday's real internet population place rows natively
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='property_descriptors';")
            if cursor.fetchone():
                # Direct SQL search tracking matches on your real data table variables
                cursor.execute("SELECT rowid, key, value, latitude, longitude FROM property_descriptors WHERE LOWER(key) LIKE ? OR LOWER(value) LIKE ? LIMIT 1500", (q, q))
                internet_rows = cursor.fetchall()
                for row in internet_rows:
                    self.data_grid.insert("", "end", values=(f"INT-{row[0]}", f"🌐 {row[1]}", row[2], row[3], row[4], "📦 Internet Sync"))
                    displayed_items_count += 1
                
                cursor.execute("SELECT COUNT(*) FROM property_descriptors")
                bulk_nodes_count = cursor.fetchone()[0]
            else:
                # Secondary backup data structural check line tracking alternative table labels
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='LL-BULK-GPK-ZON';")
                if cursor.fetchone():
                    cursor.execute("SELECT rowid, property_descriptors, landmark_clues, latitude, longitude FROM [LL-BULK-GPK-ZON] WHERE LOWER(property_descriptors) LIKE ? OR LOWER(landmark_clues) LIKE ? LIMIT 1500", (q, q))
                    bulk_rows = cursor.fetchall()
                    for brow in bulk_rows:
                        self.data_grid.insert("", "end", values=(f"INT-{brow[0]}", f"🌐 {brow[1]}", brow[2], brow[3], brow[4], "📦 Internet Sync"))
