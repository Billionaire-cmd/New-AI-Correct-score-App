import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to scrape data from SoccerStats
def get_soccerstats_data():
    url = "https://www.soccerstats.com/matches.asp?matchday=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Example: Scrape match data (you can customize this to fit your needs)
    table = soup.find("table", {"id": "btable"})
    matches = []

    if table:
        rows = table.find_all("tr")[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 1:
                match = {
                    "home_team": cols[1].text.strip(),
                    "away_team": cols[3].text.strip(),
                    "score": cols[4].text.strip(),
                }
                matches.append(match)

    return matches


# Function to scrape data from StatsChecker
def get_statschecker_data():
    url = "https://www.statschecker.com/stats/goals-per-game/average-goals-per-game-stats"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Example: Scrape average goals per game stats
    table = soup.find("table", {"class": "table"})  # Modify based on the actual class name
    stats = []

    if table:
        rows = table.find_all("tr")[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 1:
                stat = {
                    "league": cols[0].text.strip(),
                    "average_goals": cols[1].text.strip(),
                }
                stats.append(stat)

    return stats


# Streamlit App
st.title("Soccer Stats and Goals Analysis")

# Display SoccerStats data
st.header("Matches from SoccerStats")
soccerstats_data = get_soccerstats_data()
if soccerstats_data:
    for match in soccerstats_data:
        st.write(f"{match['home_team']} vs {match['away_team']} - Score: {match['score']}")
else:
    st.write("No data available from SoccerStats.")

# Display StatsChecker data
st.header("Average Goals Per Game from StatsChecker")
statschecker_data = get_statschecker_data()
if statschecker_data:
    for stat in statschecker_data:
        st.write(f"League: {stat['league']} - Avg Goals: {stat['average_goals']}")
else:
    st.write("No data available from StatsChecker.")
