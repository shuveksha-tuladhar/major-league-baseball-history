import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote

us_states = [
    'Alabama', 'Louisiana', 'Ohio', 'Alaska', 'Maine', 'Oklahoma', 'Arizona', 'Maryland', 'Oregon',
    'Arkansas', 'Massachusetts', 'Pennsylvania', 'California', 'Michigan', 'Rhode Island', 'Colorado',
    'Minnesota', 'South Carolina', 'Connecticut', 'Mississippi', 'South Dakota', 'Delaware', 'Missouri',
    'Tennessee', 'Florida', 'Montana', 'Texas', 'Georgia', 'Nebraska', 'Utah', 'Hawaii', 'Nevada', 'Vermont',
    'Idaho', 'New Hampshire', 'Virginia', 'Illinois', 'New Jersey', 'Washington', 'Indiana', 'New Mexico',
    'D.C.', 'Iowa', 'New York', 'West Virginia', 'Kansas', 'North Carolina', 'Wisconsin', 'Kentucky',
    'North Dakota', 'Wyoming'
]

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

all_data = []

for state in us_states:
    encoded_state = quote(state)
    url = f"https://www.baseball-almanac.com/players/birthplace.php?loc={encoded_state}"
    print(f"Scraping {state}...")

    driver.get(url)
    time.sleep(5)

    rows = driver.find_elements(By.XPATH, "//table[@class='boxed']//tr")

    for row in rows:
        try:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) != 5 or "player" in cols[0].text.lower():
                continue

            name = cols[0].text.strip()
            birthplace = cols[1].text.strip()
            birth_date = cols[2].text.strip()
            debut_year = cols[3].text.strip()
            final_year = cols[4].text.strip()

            debut_year = int(debut_year) if debut_year.isdigit() else None

            all_data.append({
                "name": name,
                "birth_date": birth_date,
                "birth_city": birthplace.split(",")[0].strip() if "," in birthplace else None,
                "birth_state": birthplace.split(",")[1].strip() if "," in birthplace else None,
                "debut_year": debut_year,
                "final_year": final_year,
            })

        except Exception:
            continue

driver.quit()

df = pd.DataFrame(all_data)
df.to_csv("players_by_birthplace.csv", index=False)
print("All states scraped and saved to `players_by_birthplace.csv`")
