Python: Exporting Odds to CSV and SQLite

You’ll need the requests library (pip install requests). The sqlite3 and csv modules are built into Python.

Python
import requests
import csv
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
API_KEY = 'YOUR_API_KEY'
SPORT = 'americanfootball_nfl'  # Example: NFL
REGIONS = 'us'
MARKETS = 'h2h'
FILENAME = 'sports_odds.csv'
DB_NAME = 'sports_betting.db'

def fetch_odds():
    url = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds'
    params = {
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': 'american'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def save_to_csv(data):
    # Flatten the JSON for CSV format
    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write header if file is empty
        if file.tell() == 0:
            writer.writerow(['Timestamp', 'ID', 'Home', 'Away', 'Bookmaker', 'Team', 'Price'])

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for event in data:
            for bookmaker in event['bookmakers']:
                for market in bookmaker['markets']:
                    for outcome in market['outcomes']:
                        writer.writerow([
                            timestamp, event['id'], event['home_team'], 
                            event['away_team'], bookmaker['title'], 
                            outcome['name'], outcome['price']
                        ])

def save_to_db(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS odds (
            timestamp TEXT, event_id TEXT, home_team TEXT, 
            away_team TEXT, bookmaker TEXT, selection TEXT, price REAL
        )
    ''')
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for event in data:
        for bookmaker in event['bookmakers']:
            for market in bookmaker['markets']:
                for outcome in market['outcomes']:
                    cursor.execute('''
                        INSERT INTO odds VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (timestamp, event['id'], event['home_team'], 
                          event['away_team'], bookmaker['title'], 
                          outcome['name'], outcome['price']))
    
    conn.commit()
    conn.close()

# --- EXECUTION ---
odds_data = fetch_odds()
if odds_data:
    save_to_csv(odds_data)
    save_to_db(odds_data)
    print(f"Successfully exported data to {FILENAME} and {DB_NAME}")
