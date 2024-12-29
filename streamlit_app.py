import streamlit as st
import numpy as np

# Add Team Form and Percentage Analysis
st.title("🤖🤖🤖Rabiotic Football Match Outcome Prediction")
st.sidebar.header("Team Details")

# Input Team A and Team B details
team_A = st.sidebar.text_input("Enter Team A Name:")
team_B = st.sidebar.text_input("Enter Team B Name:")

percentage_A = st.sidebar.number_input("Team A Winning Percentage (%):", min_value=0.0, max_value=100.0, step=0.1)
percentage_B = st.sidebar.number_input("Team B Winning Percentage (%):", min_value=0.0, max_value=100.0, step=0.1)

# Input Previous Meeting Outcomes
home_wins = st.sidebar.number_input(f"Previous {team_A} Home Wins vs {team_B}:", min_value=0)
draws = st.sidebar.number_input(f"Previous Draws:", min_value=0)
away_wins = st.sidebar.number_input(f"Previous {team_B} Away Wins vs {team_A}:", min_value=0)

# Calculate probabilities based on team form and previous meetings
total_meetings = home_wins + draws + away_wins
if total_meetings > 0:
    prob_home = home_wins / total_meetings
    prob_draw = draws / total_meetings
    prob_away = away_wins / total_meetings
else:
    prob_home = prob_draw = prob_away = 0

st.write(f"Team A Win Probability: **{prob_home:.2f}**")
st.write(f"Draw Probability: **{prob_draw:.2f}**")
st.write(f"Team B Win Probability: **{prob_away:.2f}**")

# Add odds input
st.sidebar.header("Odds Input")
odds_home = st.sidebar.number_input("Odds for Home Win:")
odds_draw = st.sidebar.number_input("Odds for Draw:")
odds_away = st.sidebar.number_input("Odds for Away Win:")
odds_over_1_5 = st.sidebar.number_input("Odds for Over 1.5 Goals:")
odds_under_1_5 = st.sidebar.number_input("Odds for Under 1.5 Goals:")
odds_over_2_5 = st.sidebar.number_input("Odds for Over 2.5 Goals:")
odds_under_2_5 = st.sidebar.number_input("Odds for Under 2.5 Goals:")
odds_btts_gg = st.sidebar.number_input("Odds for Both Teams to Score (GG):")
odds_btts_ng = st.sidebar.number_input("Odds for Both Teams Not to Score (NG):")

# Score matrix for Poisson distribution (example with probabilities)
score_matrix = np.array([
    [0.1, 0.2, 0.1],
    [0.15, 0.25, 0.1],
    [0.05, 0.1, 0.1]
])  # Replace with actual probabilities

# Probabilities for additional outcomes
prob_over_1_5 = 1 - (score_matrix[0, 0] + score_matrix[0, 1] + score_matrix[1, 0] + score_matrix[1, 1])
prob_under_1_5 = 1 - prob_over_1_5
prob_over_2_5 = 1 - np.sum(score_matrix[:3, :3])  # Sum of scores where total goals <= 2
prob_under_2_5 = 1 - prob_over_2_5
prob_btts_gg = np.sum(score_matrix[1:, 1:])  # Both teams score at least one goal
prob_btts_ng = 1 - prob_btts_gg

# Value bet analysis
st.subheader("Value Bet Analysis")
ev_home = (prob_home * odds_home) - 1
ev_draw = (prob_draw * odds_draw) - 1
ev_away = (prob_away * odds_away) - 1
ev_over_1_5 = (prob_over_1_5 * odds_over_1_5) - 1
ev_under_1_5 = (prob_under_1_5 * odds_under_1_5) - 1
ev_over_2_5 = (prob_over_2_5 * odds_over_2_5) - 1
ev_under_2_5 = (prob_under_2_5 * odds_under_2_5) - 1
ev_btts_gg = (prob_btts_gg * odds_btts_gg) - 1
ev_btts_ng = (prob_btts_ng * odds_btts_ng) - 1

st.write(f"Expected Value for Home Win: **{ev_home:.2f}**")
st.write(f"Expected Value for Draw: **{ev_draw:.2f}**")
st.write(f"Expected Value for Away Win: **{ev_away:.2f}**")
st.write(f"Expected Value for Over 1.5 Goals: **{ev_over_1_5:.2f}**")
st.write(f"Expected Value for Under 1.5 Goals: **{ev_under_1_5:.2f}**")
st.write(f"Expected Value for Over 2.5 Goals: **{ev_over_2_5:.2f}**")
st.write(f"Expected Value for Under 2.5 Goals: **{ev_under_2_5:.2f}**")
st.write(f"Expected Value for Both Teams to Score (GG): **{ev_btts_gg:.2f}**")
st.write(f"Expected Value for Both Teams Not to Score (NG): **{ev_btts_ng:.2f}**")

# Add a submit button to the sidebar
with st.sidebar:
    st.markdown("### Submit Prediction")
    if st.button("Submit Prediction"):
        st.success("Prediction submitted! Results will be displayed below.")
