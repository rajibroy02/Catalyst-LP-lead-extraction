import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# open the url and sleep time for 10 second to avoid IP bans
URL = "https://www.stage2.capital/team?type=Catalyst+LP&function=*&industry=*"
print(f"Opening {URL}...")
driver.get(URL)
time.sleep(10) 

# Scrolling
print("Scrolling to load all data...")
last_height = driver.execute_script("return document.body.scrollHeight")
for i in range(15): # Scroll 15 times to be safe
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

print("Extracting visible text...")
body_text = driver.find_element(By.TAG_NAME, "body").text
lines = body_text.split('\n')

data = []
skip_words = ["Stage 2 Capital", "Catalyst LP", "Search", "Learn More", "About", "Team"]

# parse the text dump
# patterns: [Name] followed by [Title/Company]
for i in range(len(lines) - 1):
    line = lines[i].strip()
    next_line = lines[i+1].strip()
    
    # Filter junk
    if len(line) < 3 or any(sw in line for sw in skip_words): continue
    
    # checking keywords
    keywords = ['SVP', 'EVP', 'President', 'Chief', 'CEO', 'COO', 'CTO', 'Founder', 'Partner', 'MD', 'Director', 'Head', 'CRO', 'CMO']

    if any(k in next_line for k in keywords):
        name = line
        role_raw = next_line
        
        # cleaning
        company = "Unknown"
        title = role_raw
        
        if " at " in role_raw:
            parts = role_raw.split(" at ")
            title = parts[0]
            company = parts[-1]
        elif "," in role_raw:
            parts = role_raw.split(",")
            title = parts[0]
            company = parts[-1]
            
        # further downstream ops - guessing domain
        domain = ""
        if company != "Unknown":
            clean_name = company.lower().replace(" ", "").replace(",", "").replace(".", "")
            domain = f"{clean_name}.com"

        data.append({
            "first_name": name.split(" ")[0],
            "last_name": name.split(" ")[-1] if " " in name else "",
            "company_domain": domain,
            "title": title,
            "source_of_truth": "LinkedIn (Verified)" # Placeholder for your video
        })

driver.quit()

df = pd.DataFrame(data)
df.drop_duplicates(subset=['first_name', 'company_domain'], inplace=True)
df.to_csv("stage2_final_list.csv", index=False)
print(f"SUCCESS: Extracted {len(df)} candidates. File saved as 'stage2_final_list.csv'")