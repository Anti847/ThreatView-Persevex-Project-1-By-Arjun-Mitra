# ThreatView - Tiered Threat Intelligence Dashboard

This is my Python based Threat Intelligence Platform that ingests open source threat feeds, normalises Indicators of Compromise (IoCs), and presents actionable insights via an interactive dashboard with PDF exporting capabilities.

## Technical Architecture
- Language - Python 3.x
- Data Ingestion Engine - Fetches, parses, and normalises live CSV threat data from URLhaus.
- Database - SQLite3 (threats.db) storing unified threat schemas.
- Frontend Dashboard - Built using Streamlit.
- Reporting Engine - Native PDF export generated via reportlab.

## Quickstart Guide

1. **Install Dependencies:**
   ```bash
   pip install requests streamlit reportlab