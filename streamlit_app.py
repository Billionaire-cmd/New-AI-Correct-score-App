import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson

# Title
st.title("Football Match Correct Score Predictor")
st.subheader("Predict the correct score based on league table statistics")

# Input League Table Data
st.sidebar.header("Input Team Statistics")
st.sidebar.write("Enter the league table statistics for Teams A and B:")

# Team A stats
team_a = st.sidebar.text_input("Team A Name", "Team A")
team_a_played = st.sidebar.number_input("Matches Played (Team A)", min_value=0, value=10)
team_a_wins = st.sidebar.number_input("Wins (Team A)", min_value=0, value=6)
team_a_draws = st.sidebar.number_input("Draws (Team A)", min_value=0, value=2)
team_a_losses = st.sidebar.number_input("Losses (Team A)", min_value=0, value=2)
team_a_goal_diff = st.sidebar.number_input("Goal Difference (Team A)", value=10)
team_a_points = st.sidebar.number_input("Points (Team A)", value=20)

# Team B stats
team_b = st.sidebar.text_input("Team B Name", "Team B")
team_b_played = st.sidebar.number_input("Matches Played (Team B)", min_value=0, value=10)
team_b_wins = st.sidebar.number_input("Wins (Team B)", min_value=0, value=7)
team_b_draws = st.sidebar.number_input("Draws (Team B)", min_value=0, value=1)
team_b_losses = st.sidebar.number_input("Losses (Team B)", min_value=0, value=2)
team_b_goal_diff = st.sidebar.number_input("Goal Difference (Team B)", value=12)
team_b_points = st.sidebar.number_input("Points (Team B)", value=22)

# Calculate average goals scored and conceded per game
team_a_avg_goals_scored = team_a_goal_diff / team_a_played if team_a_played > 0 else 0
team_a_avg_goals_conceded = (team_a_played * 2 - team_a_goal_diff) / team_a_played if team_a_played > 0 else 0

team_b_avg_goals_scored = team_b_goal_diff / team_b_played if team_b_played > 0 else 0
team_b_avg_goals_conceded = (team_b_played * 2 - team_b_goal_diff) / team_b_played if team_b_played > 0 else 0

# Display stats
st.write(f"### League Table Stats for {team_a} vs {team_b}")
st.write(f"- **{team_a}**: Played {team_a_played}, Wins {team_a_wins}, Draws {team_a_draws}, Losses {team_a_losses}, Goal Diff {team_a_goal_diff}, Points {team_a_points}")
st.write(f"- **{team_b}**: Played {team_b_played}, Wins {team_b_wins}, Draws {team_b_draws}, Losses {team_b_losses}, Goal Diff {team_b_goal_diff}, Points {team_b_points}")

# Poisson Distribution for Goal Scoring
st.write("### Predicted Goal Scoring Probabilities")
team_a_strength = team_a_avg_goals_scored / team_b_avg_goals_conceded if team_b_avg_goals_conceded > 0 else 0
team_b_strength = team_b_avg_goals_scored / team_a_avg_goals_conceded if team_a_avg_goals_conceded > 0 else 0

max_goals = 5
team_a_probs = [poisson.pmf(i, team_a_strength) for i in range(max_goals + 1)]
team_b_probs = [poisson.pmf(i, team_b_strength) for i in range(max_goals + 1)]

# Display probability matrix
prob_matrix = np.outer(team_a_probs, team_b_probs)

st.write(f"### Correct Score Probability Matrix for {team_a} vs {team_b}")
prob_df = pd.DataFrame(prob_matrix, index=[f"{team_a} {i}" for i in range(max_goals + 1)],
                       columns=[f"{team_b} {i}" for i in range(max_goals + 1)])
st.table(prob_df)

# Recommended correct score
best_score = np.unravel_index(np.argmax(prob_matrix), prob_matrix.shape)
st.write(f"### Recommended Correct Score: {team_a} {best_score[0]} - {team_b} {best_score[1]}")
