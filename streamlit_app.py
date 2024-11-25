import streamlit as st
import numpy as np
from scipy.stats import poisson
import pandas as pd

# Title and Description
st.title("Realistic Sports Betting Correct Score Predictor")
st.write("""
This app predicts correct scores, calculates probabilities for HT/FT outcomes, and provides AI-recommended bets for potential profit.
""")

# User Inputs
st.sidebar.header("Match Statistics")
home_team = st.sidebar.text_input("Home Team", "Team A")
away_team = st.sidebar.text_input("Away Team", "Team B")
avg_home_goals = st.sidebar.number_input("Home Team Avg Goals Scored", min_value=0.0, max_value=5.0, value=1.4, step=0.1)
avg_away_goals = st.sidebar.number_input("Away Team Avg Goals Scored", min_value=0.0, max_value=5.0, value=1.2, step=0.1)
odds_home_win = st.sidebar.number_input("Odds for Home Win", min_value=1.0, value=2.5)
odds_draw = st.sidebar.number_input("Odds for Draw", min_value=1.0, value=3.0)
odds_away_win = st.sidebar.number_input("Odds for Away Win", min_value=1.0, value=2.8)

# Poisson Distribution
def poisson_prob(avg_goals, max_goals=5):
    """Calculate Poisson probabilities for goals."""
    return [poisson.pmf(i, avg_goals) for i in range(max_goals+1)]

home_probs = poisson_prob(avg_home_goals)
away_probs = poisson_prob(avg_away_goals)

# Probabilities for Each Scoreline
scoreline_probs = {}
for home_goals, p_home in enumerate(home_probs):
    for away_goals, p_away in enumerate(away_probs):
        scoreline_probs[(home_goals, away_goals)] = p_home * p_away

# DataFrame for Visualization
df = pd.DataFrame.from_dict(scoreline_probs, orient='index', columns=['Probability'])
df.index = pd.MultiIndex.from_tuples(df.index, names=["Home Goals", "Away Goals"])
df = df.sort_values('Probability', ascending=False)

# Display Top Predictions
st.write("### Top Predicted Correct Scores")
st.dataframe(df.head(10))

# HT/FT Predictions
st.write("### HT/FT Predictions")
ht_probs = {}
ft_probs = {}
for (ht_home, ht_away), prob in scoreline_probs.items():
    if ht_home + ht_away < 2:  # Simplistic assumption: HT score is within first 2 goals
        ht_probs[(ht_home, ht_away)] = prob
    ft_probs[(ht_home, ht_away)] = prob

ht_probs = {k: v / sum(ht_probs.values()) for k, v in ht_probs.items()}
ft_probs = {k: v / sum(ft_probs.values()) for k, v in ft_probs.items()}

st.write("#### Top HT Outcomes")
st.write(pd.Series(ht_probs).sort_values(ascending=False).head(5))

st.write("#### Top FT Outcomes")
st.write(pd.Series(ft_probs).sort_values(ascending=False).head(5))

# BTTS (Both Teams to Score)
btts_yes = sum(prob for (h, a), prob in scoreline_probs.items() if h > 0 and a > 0)
btts_no = 1 - btts_yes

st.write("### Both Teams to Score (BTTS) Predictions")
st.write(f"BTTS - Yes: {btts_yes:.2%}")
st.write(f"BTTS - No: {btts_no:.2%}")

# AI Bet Recommendation
st.write("### AI Betting Recommendation")
best_bet = None
if odds_home_win < odds_draw and odds_home_win < odds_away_win:
    best_bet = f"Bet on Home Win ({odds_home_win})"
elif odds_away_win < odds_draw:
    best_bet = f"Bet on Away Win ({odds_away_win})"
else:
    best_bet = f"Bet on Draw ({odds_draw})"

if btts_yes > 0.5:
    st.write(f"Recommended Bet: {best_bet} with BTTS - Yes")
else:
    st.write(f"Recommended Bet: {best_bet} with BTTS - No")

# Footer
st.write("""
---
*Powered by statistical modeling and AI.*
""")
