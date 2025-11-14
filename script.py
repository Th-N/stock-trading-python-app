import requests
import os
import time
import csv
from dotenv import load_dotenv
load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
LIMIT = 1000
url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'

response = requests.get(url)
tickers = []

data = response.json()
for ticker in data['results']:
    tickers.append(ticker)


while 'next_url' in data:
    print('requesting next page', data['next_url'])
    print(data.keys())
    # passing in arguments for next url and api key
    response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
    data = response.json()
    for ticker in data['results']:
        tickers.append(ticker)
    time.sleep(12)

example_ticker = {'ticker': 'BATL', 
'name': 'Battalion Oil Corporation', 
'market': 'stocks', 
'locale': 'us', 
'primary_exchange': 'XASE', 
'type': 'CS', 
'active': True, 
'currency_name': 'usd', 
'cik': '0001282648', 
'composite_figi': 'BBG00R4SMLR4', 
'share_class_figi': 'BBG00R4SR3J8', 
'last_updated_utc': '2025-11-11T07:06:30.823232089Z'}

print(len(tickers))

# Write tickers to CSV with the same schema as example_ticker
csv_filename = 'tickers.csv'
fieldnames = list(example_ticker.keys())

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for ticker in tickers:
        # Create a row with all fields from example_ticker schema
        # Use ticker value if available, otherwise use empty string
        row = {field: ticker.get(field, '') for field in fieldnames}
        writer.writerow(row)

print(f'Successfully wrote {len(tickers)} tickers to {csv_filename}')