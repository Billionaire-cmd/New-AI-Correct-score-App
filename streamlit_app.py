import streamlit as st
import requests
from bs4 import BeautifulSoup

# Define the two URLs
URL1 = "https://www.soccerstats.com/matches.asp?matchday=1"
URL2 = "https://www.statschecker.com/stats/goals-per-game/average-goals-per-game-stats"

def fetch_soccerstats():
    """Fetch and scrape data from SoccerStats."""
    try:
        response = requests.get(URL1)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Example: Extract match details (modify selectors based on the website's structure)
        matches = []
        for row in soup.find_all("tr", class_="odd"):
            match = row.get_text(strip=True)
            matches.append(match)
        
        return matches
    except Exception as e:
        return f"Error fetching data from SoccerStats: {e}"

def fetch_statschecker():
    """Fetch and scrape data from StatsChecker."""
    try:
        response = requests.get(URL2)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Example: Extract goals-per-game stats (modify selectors based on the website's structure)
        stats = []
        for row in soup.find_all("div", class_="stats"):
            stat = row.get_text(strip=True)
            stats.append(stat)
        
        return stats
    except Exception as e:
        return f"Error fetching data from StatsChecker: {e}"

# Streamlit App UI
st.title("Football Stats Aggregator")

st.header("Data from SoccerStats")
soccer_stats = fetch_soccerstats()
if isinstance(soccer_stats, list):
    for match in soccer_stats:
        st.write(match)
else:
    st.error(soccer_stats)

st.header("Data from StatsChecker")
statschecker_data = fetch_statschecker()
if isinstance(statschecker_data, list):
    for stat in statschecker_data:
        st.write(stat)
else:
    st.error(statschecker_data)
