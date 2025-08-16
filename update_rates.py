import requests
from bs4 import BeautifulSoup
from supabase import create_client
import pandas as pd
import os
from dotenv import load_dotenv

# Load Supabase credentials
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch latest rate_date from Supabase
res = supabase.table("exchange_rates").select("rate_date").order("rate_date", desc=True).limit(1).execute()
latest_date = None
if res.data:
    latest_date = pd.to_datetime(res.data[0]["rate_date"]).date()

print(f"Latest date in DB: {latest_date}")

# Fetch the HTML page
url = "https://www.exchange-rates.org/exchange-rate-history/usd-ngn-2025"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all 'w' class elements
collection = soup.find_all(class_="w")

dates = []
rates = []
flag = True

for item in collection:
    text = item.get_text(strip=True)
    if text:
        if flag:
            dates.append(text)
            flag = False
        else:
            rates.append(text)
            flag = True

# Convert rates to floats
naira_changes = []
s = ""
for i in rates:
    for j in range(1,len(i)):
        if i[j].isdigit() or i[j] == '.':
            s+=i[j]
    n = float(s)
    naira_changes.append(n)
    s = ""
rate_dates = pd.to_datetime(dates)

# Prepare new data to upsert
new_data = []
for i in range(len(dates)):
    if rate_dates[i].date() > latest_date:
        new_data.append({
            "currency_pair": "USD/NGN",
            "rate": naira_changes[i],
            "rate_date": rate_dates[i].date().isoformat()
        })

# Upsert new rows to Supabase
if new_data:
    supabase.table("exchange_rates").upsert(new_data).execute()
    print(f"{len(new_data)} new rows upserted to Supabase.")
else:
    print("No new data to insert.")
