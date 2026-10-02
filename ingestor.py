import csv
import io
import requests
import database

# This will be a public feed that does not require an authorisation key.
URLHAUS_PUBLIC_FEED = "https://urlhaus.abuse.ch/downloads/csv_recent/"


def fetch_and_store_urlhaus_data():
    print("Fetching live threat data from the public feed. Please wait.")

    try:
        # Fetching public CSV feed
        response = requests.get(URLHAUS_PUBLIC_FEED, timeout=15)

        if response.status_code == 200:
            print("Successfully connected. Parsing CSV threat data. Please wait.")

            # This should convert raw web response text into readable text.
            lines = response.text.splitlines()

            # This will filter out comment lines like this one, basically lines starting with "#".
            csv_lines = [line for line in lines if not line.startswith('#')]

            # Reading CSV content
            csv_reader = csv.reader(csv_lines)

            saved_count = 0
            for row in csv_reader:
                if len(row) >= 8:
                    # This is the CSV column structure below -
                    # row1 = date added
                    # row2 = url
                    # row3 = url status
                    # row4 = threat
                    # row7 = reporter

                    indicator = row[2]
                    threat_type = row[4] if row[4] else "Malware / Phishing"
                    url_status = row[3] if row[3] else "Unknown"
                    reporter = row[7] if row[7] else "Anonymous"
                    date_added = row[1] if row[1] else "N/A"
                    source_feed = "URLhaus"

                    # This should transform and load into database
                    database.insert_ioc(
                        indicator=indicator,
                        threat_type=threat_type,
                        url_status=url_status,
                        reporter=reporter,
                        date_added=date_added,
                        source_feed=source_feed
                    )
                    saved_count += 1

                    # I am deliberately stopping after 100 entries for initial testing.
                    if saved_count >= 100:
                        break

            print(f"ETL Complete - {saved_count} records saved to database.")
        else:
            print(f"Failed to fetch data. HTTP Status Code - {response.status_code}")

    except requests.RequestException as e:
        print(f"Network error during ingestion - {e}")


if __name__ == "__main__":
    # I am ensuring the database table exists before ingesting with this line.
    database.init_db()

    # Running the ETL script.
    fetch_and_store_urlhaus_data()