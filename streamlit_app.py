import streamlit as st
import numpy as np
from scipy.stats import poisson

# Function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate the implied probability from odds
def implied_prob(odds):
    return 1 / odds * 100

# Function to calculate probabilities for all scorelines
def calculate_scoreline_probs(home_goals_dist, away_goals_dist, max_goals):
    scoreline_probs = {}
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            prob = home_goals_dist.pmf(i) * away_goals_dist.pmf(j)
            scoreline_probs[f"{i}-{j}"] = prob
    return scoreline_probs

# Function to calculate probabilities for over/under 2.5 goals
def calculate_over_under_probs(home_goals_dist, away_goals_dist, max_goals, threshold=2.5):
    over_prob = sum(
        home_goals_dist.pmf(i) * away_goals_dist.pmf(j)
        for i in range(max_goals + 1) for j in range(max_goals + 1) if i + j > threshold
    ) * 100
    under_prob = 100 - over_prob
    return over_prob, under_prob

# Main app
def main():
    st.title("Football Match Outcome Predictor")

    # Team Inputs
    st.subheader("Team Statistics")
    team_a_name = st.text_input("Team A Name", "Home Team")
    team_b_name = st.text_input("Team B Name", "Away Team")
    team_a_avg_goals = st.number_input(f"{team_a_name} Average Goals Scored", min_value=0.0, value=1.5)
    team_b_avg_goals = st.number_input(f"{team_b_name} Average Goals Scored", min_value=0.0, value=1.2)
    team_a_conceded = st.number_input(f"{team_a_name} Average Goals Conceded", min_value=0.0, value=1.0)
    team_b_conceded = st.number_input(f"{team_b_name} Average Goals Conceded", min_value=0.0, value=1.1)

    # Maximum goals for scoreline calculation
    max_goals = st.slider("Maximum Goals for Correct Scoreline Calculation", min_value=1, max_value=10, value=5)

    # Odds Inputs
    st.sidebar.subheader("Odds Inputs")
    over_2_5_odds = st.sidebar.number_input("Over 2.5 Goals Odds", min_value=1.0, value=1.5)
    under_2_5_odds = st.sidebar.number_input("Under 2.5 Goals Odds", min_value=1.0, value=2.5)

    # Expected Goals
    home_expected_goals = team_a_avg_goals * (team_b_conceded / 1.5)
    away_expected_goals = team_b_avg_goals * (team_a_conceded / 1.5)

    # Calculate Poisson distributions
    home_goals_dist = poisson(home_expected_goals)
    away_goals_dist = poisson(away_expected_goals)

    # Calculate correct score probabilities
    scoreline_probs = calculate_scoreline_probs(home_goals_dist, away_goals_dist, max_goals)

    # Calculate over/under 2.5 goals probabilities
    over_2_5_prob, under_2_5_prob = calculate_over_under_probs(home_goals_dist, away_goals_dist, max_goals)

    # Display Results
    st.subheader("Predicted Probabilities")
    st.write(f"**Expected Goals for {team_a_name}:** {home_expected_goals:.2f}")
    st.write(f"**Expected Goals for {team_b_name}:** {away_expected_goals:.2f}")
    st.write(f"**Over 2.5 Goals Probability:** {over_2_5_prob:.2f}%")
    st.write(f"**Under 2.5 Goals Probability:** {under_2_5_prob:.2f}%")

    # Display correct score probabilities
    st.subheader("Correct Score Probabilities")
    scorelines = sorted(scoreline_probs.items(), key=lambda x: x[1], reverse=True)
    for score, prob in scorelines[:10]:
        st.write(f"{score}: {prob * 100:.2f}%")

    # Display all scorelines in a table
    st.write("**All Scoreline Probabilities**")
    score_table = {score: f"{prob * 100:.2f}%" for score, prob in scoreline_probs.items()}
    st.table(score_table)

if __name__ == "__main__":
    main()
