# from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import psycopg2
from datetime import date
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)
# Replace with your Supabase credentials


# the options part is to prevent the driver from automatically popping up the chrome browser
# ######### If there's an error about the webdriver, reinstall webdriver_manager ##########
# This is to initialize option to avoid the chrome browser from popping up
option = webdriver.ChromeOptions()
option.add_argument('headless')

#website to be scraped
url = "https://www.exchange-rates.org/exchange-rate-history/usd-ngn-2025"

#open chrome and go to the url then sleep for 5 secs for the url to finish loading
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
sleep(5)

#get all the links(url) for each year, then store them in a list
unordered_list = driver.find_element(By.CLASS_NAME, 'rates-by-year')
a_elements = unordered_list.find_elements(By.TAG_NAME,"a")
links = []
for link in a_elements:
    links.append(str(link.get_attribute("href")))

#get all the dates and rates for each year then store them inside the dates and rates lists
dates = []
rates = []
help = len(links)-1
while help >= 0:
    url = links[help]
    driver.get(url)
    sleep(5)
    collection = driver.find_elements(By.CLASS_NAME, 'w')
    flag = True
    for data in collection:
        if flag:
            dates.append(str(data.text))
            flag = False
        else:
            rates.append(str(data.text))
            flag = True
    help-=1

driver.quit()

# parse all the strings in the rates list and then convert it to ints, and store it in naira_changes
naira_changes = []
s = ""
for i in rates:
    for j in range(1,len(i)):
        if i[j].isdigit() or i[j] == '.':
            s+=i[j]
    n = float(s)
    naira_changes.append(n)
    s = ""
    

# plotting of the graph    
formatted_dates = pd.to_datetime(dates)
data_batch = [
    {
        "currency_pair": "USD/NGN",
        "rate": naira_changes[i],
        "rate_date": formatted_dates[i].date().isoformat()
    }
    for i in range(len(formatted_dates))
]

supabase.table("exchange_rates").upsert(data_batch).execute()

# plt.plot(formatted_dates,naira_changes)
# year_starts = pd.date_range(start=formatted_dates.min(), end=formatted_dates.max(), freq='YS')
# plt.xticks(year_starts.to_pydatetime(), year_starts.strftime("%Y"), rotation=0)
# plt.grid(True)  
# plt.xlabel("Dates")
# plt.ylabel("Exchange rates (₦/USD)")
# plt.title("Nigerian exchange rate")
# plt.show()






# email = driver.find_element(By.ID, 'listing-email')
# company = driver.find_elements(By.TAG_NAME, 'h1')


# l = driver.find_elements("xpath", '//div[@class="subb-bx MT-15"]/p[1]/a[1]')

# nextbtn = driver.find_element(By.CLASS_NAME, 'ant-pagination-next')
# nextbtn.click()

# rates_2025 = []
    # i = 0
    # while i < len(dates):
    #     rates_2025.append(str(dates[i]) + "--->" + str(rates[i]))
    #     i +=1

    # for data in rates_2025:
    #     print(data)

    # print(len(rates_2025))
