import sqlite3
import streamlit as st
import pdf_generator

DB_NAME = "threats.db"

def fetch_threat_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT indicator, threat_type, url_status, reporter, date_added, source_feed FROM threat_iocs")
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_metrics():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM threat_iocs")
    total_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM threat_iocs WHERE url_status = 'online'")
    online_count = cursor.fetchone()[0]
    conn.close()
    return total_count, online_count

def search_db(query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    search_pattern = f"%{query}%"
    cursor.execute('''
        SELECT indicator, threat_type, url_status, reporter, date_added, source_feed 
        FROM threat_iocs 
        WHERE indicator LIKE ? OR threat_type LIKE ? OR reporter LIKE ?
    ''', (search_pattern, search_pattern, search_pattern))
    results = cursor.fetchall()
    conn.close()
    return results

# User Interface Setup
st.set_page_config(page_title="ThreatView Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ ThreatView - Threat Intelligence Dashboard")
st.markdown("Real time aggregation of open source IoCs from public security feeds.")

total_threats, active_threats = fetch_metrics()

# Metrics and Report Download
st.divider()
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

with col1:
    st.metric(label="Total Ingested IoCs", value=total_threats)

with col2:
    st.metric(label="Active / Online Threats", value=active_threats)

with col3:
    st.metric(label="Primary Feed Source", value="URLhaus")

with col4:
    st.write("Export Report")
    if st.button("Generate PDF Summary"):
        pdf_path = pdf_generator.generate_pdf_report()
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="Download PDF",
                data=file,
                file_name="ThreatView_Summary.pdf",
                mime="application/pdf"
            )

st.divider()

# Search Engine
st.subheader("IoC Lookup & Threat Alert Engine")
st.markdown("Paste a suspicious domain, IP address, or file path below to verify if it appears in active threat feeds.")

user_search = st.text_input("Enter IoC Query - ", "")

if user_search:
    matches = search_db(user_search)
    if matches:
        st.error(f"**ALERT MATCH FOUND** Query **'{user_search}'** was flagged in {len(matches)} active threat record(s).")
        matched_data = []
        for row in matches:
            matched_data.append({
                "Flagged Indicator": row[0],
                "Threat Type": row[1],
                "Status": row[2],
                "Reporter": row[3],
                "Date Added": row[4],
                "Source Feed": row[5]
            })
        st.table(matched_data)
    else:
        st.success(f"**NO MATCH FOUND:** Query **'{user_search}'** does not match any current IoCs in the local database.")

st.divider()

# --- RECENT INDICATORS DATA TABLE ---
st.subheader("Recent IoCs")

data = fetch_threat_data()

if data:
    formatted_data = []
    for row in data:
        formatted_data.append({
            "Indicator (URL / Host)": row[0],
            "Threat Type": row[1],
            "Status": row[2],
            "Reporter": row[3],
            "Date Added": row[4],
            "Source": row[5]
        })
    st.dataframe(formatted_data, use_container_width=True)
else:
    st.warning("No threat data found in database. Make sure you ran ingestor.py first!")