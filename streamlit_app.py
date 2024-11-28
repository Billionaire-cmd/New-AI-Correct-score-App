import streamlit as st
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


# Function to scrape data from SoccerStats
def get_soccerstats_data():
    url = "https://www.soccerstats.com/matches.asp?matchday=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        st.error(f"Error fetching data from SoccerStats: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "btable"})  # Modify as needed
    matches = []

    if table:
        rows = table.find_all("tr")[1:]  # Skip header row
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


# Function to scrape data from StatsChecker using Selenium
def get_statschecker_data():
    url = "https://www.statschecker.com/stats/goals-per-game/average-goals-per-game-stats"

    # Set up Selenium WebDriver (ensure you have downloaded ChromeDriver)
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver_service = Service("path/to/chromedriver")  # Replace with the path to your ChromeDriver
    driver = webdriver.Chrome(service=driver_service, options=options)

    stats = []
    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # Scrape table data
        rows = driver.find_elements(By.XPATH, "//table[@class='table']/tbody/tr")
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) > 1:
                stat = {
                    "league": cols[0].text.strip(),
                    "average_goals": cols[1].text.strip(),
                }
                stats.append(stat)
    except Exception as e:
        st.error(f"Error fetching data from StatsChecker: {e}")
    finally:
        driver.quit()

    return stats


# Streamlit App
st.title("Soccer and Stats Analysis")

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
