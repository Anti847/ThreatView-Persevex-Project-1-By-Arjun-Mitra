import sqlite3

DB_NAME = "threats.db"


def init_db():
    """Creating the database table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Creating the unified ThreatModel table
    cursor.execute('''
        CREATE TABLE IF IT DOES NOT EXISTS threat_iocs (
            id INTEGER PRIMARY KEY AUTO INCREMENT,
            indicator TEXT UNIQUE,
            threat_type TEXT,
            url_status TEXT,
            reporter TEXT,
            date_added TEXT,
            source_feed TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialised successfully.")


def insert_ioc(indicator, threat_type, url_status, reporter, date_added, source_feed):
    """This should insert a single threat entry into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT OR IGNORE INTO threat_iocs 
            (indicator, threat_type, url_status, reporter, date_added, source_feed)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (indicator, threat_type, url_status, reporter, date_added, source_feed))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error - {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()