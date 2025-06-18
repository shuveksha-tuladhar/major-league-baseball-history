import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Baseball Players by Birthplace", layout="wide")
st.title("Baseball Players Birthplace Explorer")

# Load data
@st.cache_data
def load_data():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql_query("SELECT * FROM players_birthplace", conn)
    conn.close()
    
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Players")
states = sorted(df["state"].dropna().unique())
selected_state = st.sidebar.selectbox("Select a U.S. State", states)

# Convert birth_date to datetime and extract birth year
df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")
df["birth_year"] = df["birth_date"].dt.year

min_year, max_year = int(df["debut_year"].min()), int(df["debut_year"].max())
year_range = st.sidebar.slider("Debut Year Range", min_value=min_year, max_value=max_year,
                               value=(min_year, max_year), step=1)

birth_min_year, birth_max_year = int(df["birth_year"].min()), int(df["birth_year"].max())
birth_year_range = st.sidebar.slider("Birth Year Range", min_value=birth_min_year, max_value=birth_max_year,
                               value=(birth_min_year, birth_max_year), step=1)
 
# Filtered data
filtered_df = df[
    (df["state"] == selected_state) &
    (df["debut_year"].between(year_range[0], year_range[1])) &
    (df["birth_year"].between(birth_year_range[0], birth_year_range[1]))

]

st.markdown(f"### 🎯 Showing {len(filtered_df)} players born in **{selected_state}** between {year_range[0]} and {year_range[1]}")

# Display table
st.dataframe(filtered_df, use_container_width=True)

# Show Stats
st.markdown("### 📊 Stats")
col1, col2 = st.columns(2)
col1.metric("Total Players", len(filtered_df))
col2.metric("Unique Debut Years", filtered_df['debut_year'].nunique())


# Mapping from full state names to abbreviations for Plotly
state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
    'D.C.': 'DC'
}

# Clean data: count players per state
df["state_abbrev"] = df["state"].map(state_abbrev)
state_counts = df["state_abbrev"].value_counts().rename_axis("state").reset_index(name="num_players")
state_counts["num_players_display"] = state_counts["num_players"].apply(
    lambda x: "500+" if x > 500 else str(x)
)

# Assuming state_counts["num_players"] is numeric
bins = [0, 50, 100, 200, 300, 400, 500, float('inf')]
labels = ["0–50", "51–100", "101–200", "201–300", "301–400", "401–500", "500+"]

state_counts["range_bin"] = pd.cut(
    state_counts["num_players"],
    bins=bins,
    labels=labels,
    include_lowest=True,
    right=True
)

# Convert range_bin to string for consistent mapping
state_counts["range_bin"] = state_counts["range_bin"].astype(str)

# Plotly choropleth
fig = px.choropleth(
    state_counts,
    locations="state",
    locationmode="USA-states",
    color="range_bin",
    scope="usa",
    color_continuous_scale="Blues",
    labels={"num_players": "Number of Players", "range_bin": "Range"},
    title="Number of Baseball Players Born by U.S. State",
    hover_name="state",
    hover_data={"num_players": True, "num_players_display": False, "state": False, "range_bin": True}
)

st.plotly_chart(fig, use_container_width=True)

