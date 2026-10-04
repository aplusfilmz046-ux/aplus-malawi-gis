import os
import shutil
import zipfile
import datetime
import sqlite3
from transaction_logger import log_system_event

def run_infrastructure_backup():
    db_filename = "malawi_addresses.db"
    backup_dir = "backups"
    
    print("\n=======================================================")
    print("💾 MALAWI GIS ENGINE AUTOMATED BACKUP SERVICE 💾")
    print("=======================================================\n")
    
    # 1. Verification Guard: Ensure the source database actually exists
    if not os.path.exists(db_filename):
        print(f"❌ [BACKUP CRITICAL] Source database file '{db_filename}' not found!")
        log_system_event("BACKUP_FAIL", "Database file missing. Aborting archive routine.")
        return
        
    # 2. Structure Guard: Ensure the backup directory folder exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"[SYSTEM] Created missing recovery target folder: '{backup_dir}/'")

    # 3. Time Matrix: Generate a highly clear, date-stamped file name string
    # Format: backup_YYYYMMDD_HHMMSS.zip
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = os.path.join(backup_dir, f"backup_{timestamp}.zip")
    
    try:
        print("[SYSTEM] Verifying target database file health structure...")
        
        # Test file health by quickly opening the database connection safely
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        health_status = cursor.fetchone()[0]
        conn.close()
        
        if health_status != "ok":
            print(f"❌ [BACKUP ABORTED] Database file corruption detected: {health_status}")
            log_system_event("BACKUP_CORRUPT", f"Aborted backup due to database integrity failure: {health_status}")
            return
            
        print("✅ Database file integrity check passed. Packaging files...")
        
        # 4. Packaging Core: Write the database file into a compressed zip file structure
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(db_filename)
            
        print("\n" + "="*60)
        print("✅ BACKUP TRANSACTION ARCHIVE TRANSACTION COMPLETE")
        print(f"--> Archive File Location : {zip_filename}")
        print(f"--> Compressed File Size  : {round(os.path.getsize(zip_filename) / 1024, 2)} KB")
        print("="*60)
        
        # Write to system logs
        log_system_event("SYS_BACKUP", f"Compressed archive created successfully: {os.path.basename(zip_filename)}")
        
    except Exception as error:
        print(f"❌ [BACKUP FAILED] System compression failure encountered: {error}")
        log_system_event("BACKUP_ERROR", f"System archive failure: {str(error)}")

if __name__ == "__main__":
    run_infrastructure_backup()
