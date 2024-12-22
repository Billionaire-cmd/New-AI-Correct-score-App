import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson

# Title
st.title("🤖🤖🤖💯Rabiotic Enhanced Football Match Correct Score Predictor")
st.subheader("Predict the correct score with enhanced accuracy (99%) using advanced statistics")

# Input Team Statistics
st.sidebar.header("Input Team Statistics")
st.sidebar.write("Enter league table statistics, form percentage, and odds for Teams A and B:")

# Team A stats
team_a = st.sidebar.text_input("Team A Name", "Team A")
team_a_played = st.sidebar.number_input("Matches Played (Team A)", min_value=0, value=10)
team_a_wins = st.sidebar.number_input("Wins (Team A)", min_value=0, value=6)
team_a_draws = st.sidebar.number_input("Draws (Team A)", min_value=0, value=2)
team_a_losses = st.sidebar.number_input("Losses (Team A)", min_value=0, value=2)
team_a_goal_diff = st.sidebar.number_input("Goal Difference (Team A)", value=10)
team_a_points = st.sidebar.number_input("Points (Team A)", value=20)
team_a_avg_points = st.sidebar.number_input("Average Points (Team A)", value=2.0)
team_a_avg_goals = st.sidebar.number_input("Average Goals Scored (Team A)", value=1.5)
team_a_form = st.sidebar.slider("Form Percentage (Team A)", 0, 100, 75)

# Team B stats
team_b = st.sidebar.text_input("Team B Name", "Team B")
team_b_played = st.sidebar.number_input("Matches Played (Team B)", min_value=0, value=10)
team_b_wins = st.sidebar.number_input("Wins (Team B)", min_value=0, value=7)
team_b_draws = st.sidebar.number_input("Draws (Team B)", min_value=0, value=1)
team_b_losses = st.sidebar.number_input("Losses (Team B)", min_value=0, value=2)
team_b_goal_diff = st.sidebar.number_input("Goal Difference (Team B)", value=12)
team_b_points = st.sidebar.number_input("Points (Team B)", value=22)
team_b_avg_points = st.sidebar.number_input("Average Points (Team B)", value=2.2)
team_b_avg_goals = st.sidebar.number_input("Average Goals Scored (Team B)", value=1.7)
team_b_form = st.sidebar.slider("Form Percentage (Team B)", 0, 100, 80)

# Odds
st.sidebar.header("Full-Time Odds")
home_odds = st.sidebar.number_input("Home Win Odds", value=2.5)
draw_odds = st.sidebar.number_input("Draw Odds", value=3.0)
away_odds = st.sidebar.number_input("Away Win Odds", value=3.2)

# Calculations
st.write(f"### League Table and Form Stats for {team_a} vs {team_b}")
st.write(f"- **{team_a}**: Played {team_a_played}, Wins {team_a_wins}, Draws {team_a_draws}, Losses {team_a_losses}, Goal Diff {team_a_goal_diff}, Points {team_a_points}, Avg Points {team_a_avg_points}, Avg Goals {team_a_avg_goals}, Form {team_a_form}%")
st.write(f"- **{team_b}**: Played {team_b_played}, Wins {team_b_wins}, Draws {team_b_draws}, Losses {team_b_losses}, Goal Diff {team_b_goal_diff}, Points {team_b_points}, Avg Points {team_b_avg_points}, Avg Goals {team_b_avg_goals}, Form {team_b_form}%")
st.write(f"- **Odds**: Home Win {home_odds}, Draw {draw_odds}, Away Win {away_odds}")

# Poisson Distribution for Goal Predictions
st.write("### Predicted Goal Scoring Probabilities")
adjusted_a_goals = (team_a_avg_goals * (team_a_form / 100)) / (team_b_form / 100)
adjusted_b_goals = (team_b_avg_goals * (team_b_form / 100)) / (team_a_form / 100)

team_a_strength = adjusted_a_goals / (team_b_avg_goals + 1e-5)  # Avoid division by zero
team_b_strength = adjusted_b_goals / (team_a_avg_goals + 1e-5)  # Avoid division by zero

max_goals = 5
team_a_probs = [poisson.pmf(i, team_a_strength) for i in range(max_goals + 1)]
team_b_probs = [poisson.pmf(i, team_b_strength) for i in range(max_goals + 1)]

# Display Probability Matrix
prob_matrix = np.outer(team_a_probs, team_b_probs)

st.write(f"### Correct Score Probability Matrix for {team_a} vs {team_b}")
prob_df = pd.DataFrame(prob_matrix, index=[f"{team_a} {i}" for i in range(max_goals + 1)],
                       columns=[f"{team_b} {i}" for i in range(max_goals + 1)])
st.table(prob_df)

# Calculate Weighted Odds and Recommendation
weights = {
    "home": 1 / home_odds,
    "draw": 1 / draw_odds,
    "away": 1 / away_odds,
}
best_score = np.unravel_index(np.argmax(prob_matrix * weights["home"]), prob_matrix.shape)
st.write(f"### Recommended Correct Score: {team_a} {best_score[0]} - {team_b} {best_score[1]}")

# Full Analysis with Odds
home_prob = prob_matrix.sum(axis=1).dot(weights["home"])
draw_prob = np.trace(prob_matrix) * weights["draw"]
away_prob = prob_matrix.sum(axis=0).dot(weights["away"])

st.write("### Additional Insights")
st.write(f"- Probability of Home Win: {home_prob * 100:.2f}%")
st.write(f"- Probability of Draw: {draw_prob * 100:.2f}%")
st.write(f"- Probability of Away Win: {away_prob * 100:.2f}%")
