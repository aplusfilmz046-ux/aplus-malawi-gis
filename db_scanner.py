import os
import sqlite3

def scan_for_address_data():
    print("🔍 [A+Malawi Database Hunter Active]")
    print("==================================================")
    
    # 📂 List of standard folders and files to look through
    search_folder = r"D:\maping"
    found_any = False
    
    if not os.path.exists(search_folder):
        print(f"❌ Folder directory '{search_folder}' does not exist on disk.")
        return

    # Automatically walks through your entire D:\maping workspace to find any database file
    for root, dirs, files in os.walk(search_folder):
        for file in files:
            if file.endswith('.db'):
                db_path = os.path.join(root, file)
                print(f"\n📂 FOUND DATA LEDGER DISK NODE at:\n   {db_path}")
                found_any = True
                
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    # Discover all table structures sitting inside this specific file asset
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    
                    if not tables:
                        print("   ⚠️ This database file is completely empty (no tables found).")
                        continue
                        
                    for table_tuple in tables:
                        table_name = table_tuple[0]
                        
                        # Count total address rows recorded inside this table ledger
                        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                        row_count = cursor.fetchone()[0]
                        print(f"   🔹 Table: [{table_name}] ➔ Contains ({row_count}) total rows.")
                        
                        # Print every single address collected inside the file natively!
                        if row_count > 0:
                            cursor.execute(f"SELECT * FROM {table_name}")
                            print("   📝 ALL DETECTED ENTRIES LEDGER ROWS:")
                            for row in cursor.fetchall():
                                print(f"     ➔ {row}")
                    conn.close()
                except Exception as e:
                    print(f"   ⚠️ Could not read this specific database file node: {e}")

    if not found_any:
        print("❌ Scan finished: No database (.db) files discovered inside your D:\\maping workspace.")

if __name__ == "__main__":
    scan_for_address_data()
