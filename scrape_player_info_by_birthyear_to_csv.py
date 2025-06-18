# scrape_players_by_year.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from datetime import datetime

def reformat_date(date_str):
    """Convert mm-dd-yyyy to yyyy-mm-dd, return None if empty or invalid."""
    if not date_str or date_str.lower() in ("still living", ""):
        return None
    try:
        dt = datetime.strptime(date_str, "%m-%d-%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return None
    
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

years = [
    1835, 1836, 1840, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1850,
    1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862,
    1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874,
    1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886,
    1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898,
    1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910,
    1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922,
    1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934,
    1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946,
    1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958,
    1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970,
    1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982,
    1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994,
    1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004
]

all_data = []

for year in years:
    print(f"Scraping {year}...")
    url = f"https://www.baseball-almanac.com/players/baseball_births.php?y={year}"
    driver.get(url)
    time.sleep(4)

    try:
        rows = driver.find_elements(By.XPATH, "//table[@class='boxed']//tr")
        for row in rows:
            try:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) != 5 or any("player" in col.text.lower() for col in cols):
                    continue

                name = cols[0].text.strip()
                birth_date = cols[1].text.strip()
                died_on = cols[2].text.strip()
                debut_year = cols[3].text.strip()
                final_year = cols[4].text.strip()

                all_data.append({
                    "name": name,
                    "birth_date": reformat_date(birth_date),
                    "died_date": None if died_on.lower() == "still living" else reformat_date(died_on),
                    "debut_year": int(debut_year) if debut_year.isdigit() else None,
                    "still_active": final_year.lower() == "active"
                })
            except Exception:
                continue
    except Exception as e:
        print(f"❌ Failed for {year}: {e}")
        continue

driver.quit()

df = pd.DataFrame(all_data)
df.to_csv("players_by_birthyear.csv", index=False)
print("Data saved to players_by_year.csv")
