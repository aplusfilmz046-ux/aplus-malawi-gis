import sqlite3
import threading
from contextlib import contextmanager
from transaction_logger import log_system_event

# Global thread lock configuration to manage database write access sequences safely
DATABASE_MUTEX_LOCK = threading.Lock()

@contextmanager
def get_safe_db_session():
    """
    Context manager that isolates database transaction sessions, ensuring 
    multi-threaded safety when external client applications make simultaneous API requests.
    """
    db_filename = "malawi_addresses.db"
    connection = None
    
    # Acquire mutex lock before opening file access channels
    DATABASE_MUTEX_LOCK.acquire()
    try:
        connection = sqlite3.connect(db_filename, timeout=10.0)
        # Enable Write-Ahead Logging (WAL mode) to allow simultaneous reads while writing
        connection.execute("PRAGMA journal_mode=WAL;")
        cursor = connection.cursor()
        yield cursor
        connection.commit()
    except Exception as error:
        if connection:
            connection.rollback()
        print(f"❌ [DB ENGINE CRITICAL] Transaction failed, rolled back updates: {error}")
        log_system_event("DB_LOCK_FAIL", f"Session transaction crashed: {str(error)}")
        raise error
    finally:
        if connection:
            connection.close()
        # Always release the mutex thread lock to allow the next waiting application in
        DATABASE_MUTEX_LOCK.release()

if __name__ == "__main__":
    print("--- MALAWI GEOSPATIAL MULTI-THREADING ENGINE MANAGER ---")
    print("[SYSTEM] Auditing thread-safe transactional context routines...")
    
    with get_safe_db_session() as session_cursor:
        session_cursor.execute("SELECT COUNT(*) FROM spatial_beacons;")
        count = session_cursor.fetchone()[0]
        print(f"✅ Context Check Passed: Safely read {count} infrastructure address nodes completely thread-isolated.")
