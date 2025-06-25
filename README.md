# Baseball Players Birthplace Explorer 

This project is a complete data pipeline and interactive dashboard that explores the birthplace and debut trends of U.S. baseball players. It involves **web scraping**, **data cleaning**, **SQLite integration**, and a **Streamlit** web app powered by **Plotly** visualizations.

## Live Demo

🔗 [Check out the Streamlit App](https://major-league-baseball-history.streamlit.app/)

*Explore interactive maps, charts, and filters for baseball player data!*

## Features

- Web scraping using **Selenium**
- Data storage in **CSV** and **SQLite**
- Data cleaning and transformation using **Pandas**
- Interactive dashboard built with **Streamlit**
- Visualizations with **Plotly**
- Filters by U.S. state, debut year range, and birth year range
- Choropleth map, line chart, and bar chart
- Clean layout, responsive design

##  Dashboard Preview
- Select a U.S. state from the sidebar
- Filter players by birth year and debut year
- View:
    - Filtered table of players
    - Choropleth map of player birth states
    - Line chart of birth trends
    - Bar chart of debut decade

## Data Cleaning Highlights
- Converted inconsistent date formats (MM-DD-YYYY → YYYY-MM-DD)
- Removed duplicates and null entries
- Mapped full state names to abbreviations for mapping
- Grouped data by year and decade for time-series analysis

## Dependencies
- pandas
- selenium
- streamlit
- plotly
- sqlite3

See requirements.txt for full list.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/shuveksha-tuladhar/major-league-baseball-history
```
### 2. Install Dependencies
```pip install -r requirements.txt```

### 3. Scrape the Data (Optional - already included)
```
python scrape_players_by_year.py
python scrape_players_by_state.py
```

### 4. Create the Database
```
python import_csv_to_db.py
```

### 5. Run the Streamlit App Locally
```
streamlit run app.py
```

## Data Source
All data was scraped from:
[Baseball Almanac](https://www.baseball-almanac.com)

### License
This project is for educational purposes and uses publicly available data.