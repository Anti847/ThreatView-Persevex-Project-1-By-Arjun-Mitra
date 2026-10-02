import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DB_NAME = "threats.db"


def generate_pdf_report(filename="ThreatView_Executive_Summary.pdf"):
    """This should inspect the database and generate a PDF summary report."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fetching total metrics.
    cursor.execute("SELECT COUNT(*) FROM threat_iocs")
    total_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM threat_iocs WHERE url_status = 'online'")
    online_count = cursor.fetchone()[0]

    # Fetching the most recent 10 threats.
    cursor.execute("SELECT indicator, threat_type, url_status, date_added FROM threat_iocs LIMIT 10")
    recent_rows = cursor.fetchall()
    conn.close()

    # Creating the ReportLab PDF Canvas.
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title of the PDF.
    c.setFont("Arial-Bold", 20)
    c.drawString(50, height - 50, "ThreatView - Executive Threat Report")

    c.setFont("Arial", 10)
    c.drawString(50, height - 70, "Automated Threat Intelligence Summary")
    c.line(50, height - 80, width - 50, height - 80)

    # This is the executive overview section
    c.setFont("Arial-Bold", 14)
    c.drawString(50, height - 110, "1) Executive Summary")

    c.setFont("Arial", 11)
    c.drawString(70, height - 130, f"• Total Ingested IoCs - {total_count}")
    c.drawString(70, height - 150, f"• Active/Online Malicious URLs - {online_count}")
    c.drawString(70, height - 170, "• Primary Threat Feed - URLhaus")

    # Adding recent indicators section
    c.setFont("Arial-Bold", 14)
    c.drawString(50, height - 210, "2) Top 10 Sample Ingested Indicators")

    y_pos = height - 235
    c.setFont("Arial-Bold", 9)
    c.drawString(50, y_pos, "Status")
    c.drawString(100, y_pos, "Type")
    c.drawString(200, y_pos, "Indicator or Domain")

    c.setFont("Arial", 8)
    for row in recent_rows:
        y_pos -= 18
        status, threat_type, indicator = row[2], row[1], row[0]

        # This will shorten long URLs for PDF readability.
        short_indicator = indicator[:55] + "..." if len(indicator) > 55 else indicator

        c.drawString(50, y_pos, str(status))
        c.drawString(100, y_pos, str(threat_type)[:18])
        c.drawString(200, y_pos, short_indicator)

        if y_pos < 50:
            break

    # Footer
    c.setFont("Arial-Oblique", 8)
    c.drawString(50, 30, "Generated automatically via ThreatView Python ETL Engine.")

    c.save()
    return filename


if __name__ == "__main__":
    file_created = generate_pdf_report()
    print(f"PDF generated successfully - {file_created}")