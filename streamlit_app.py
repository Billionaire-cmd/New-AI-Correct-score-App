import streamlit as st
import numpy as np
from scipy.stats import poisson, skellam

# Define the function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate the implied probability from odds
def implied_prob(odds):
    return 1 / odds * 100

# Function to calculate the odds-based probabilities (adjusted for over 2.5 goals)
def adjust_for_over_2_5_goals(over_2_5_odds, poisson_prob):
    over_2_5_prob = implied_prob(over_2_5_odds)
    adjusted_prob = poisson_prob * (over_2_5_prob / 100)
    return adjusted_prob

# Generate all possible scorelines for both HT and FT
def generate_scorelines(max_goals=5):
    scorelines = []
    for home_goals in range(max_goals + 1):
        for away_goals in range(max_goals + 1):
            scorelines.append((home_goals, away_goals))
    return scorelines

# Main function to calculate and display predictions
def calculate_predictions():
    # User input: Team A and Team B stats
    team_a_home_goals = st.number_input("Team A Average Goals Scored (Home)", min_value=0.0, value=0.30)
    team_b_away_goals = st.number_input("Team B Average Goals Scored (Away)", min_value=0.0, value=1.00)
    team_a_home_conceded = st.number_input("Team A Average Goals Conceded (Home)", min_value=0.0, value=1.50)
    team_b_away_conceded = st.number_input("Team B Average Goals Conceded (Away)", min_value=0.0, value=2.00)

    # Sidebar inputs for odds
    st.sidebar.subheader("Odds Inputs")
    ht_home_odds = st.sidebar.number_input("HT Home Odds", min_value=0.0, value=4.10)
    ht_draw_odds = st.sidebar.number_input("HT Draw Odds", min_value=0.0, value=2.25)
    ht_away_odds = st.sidebar.number_input("HT Away Odds", min_value=0.0, value=2.70)
    ft_home_odds = st.sidebar.number_input("FT Home Odds", min_value=0.0, value=3.50)
    ft_draw_odds = st.sidebar.number_input("FT Draw Odds", min_value=0.0, value=3.70)
    ft_away_odds = st.sidebar.number_input("FT Away Odds", min_value=0.0, value=2.14)
    over_2_5_odds = st.number_input("Over 2.5 Goals Odds", min_value=1.0, value=1.92)
    st.sidebar.header("Input Parameters")

    # Generate all possible scorelines (for both HT and FT)
    max_goals = 5  # Define the maximum number of goals to consider for scorelines
    ht_scorelines = generate_scorelines(max_goals)
    ft_scorelines = generate_scorelines(max_goals)

    # Calculate Poisson probabilities for each scoreline
    team_a_ht_goal_rate = team_a_home_goals / 2  # Approximate halftime goals
    team_b_ht_goal_rate = team_b_away_goals / 2  # Approximate halftime goals
    team_a_ft_goal_rate = team_a_home_goals  # Full-time goal rate
    team_b_ft_goal_rate = team_b_away_goals  # Full-time goal rate

    # Initialize lists to store results
    ht_results = []
    ft_results = []

    # Calculate Poisson probabilities for HT scorelines
    for home_goals, away_goals in ht_scorelines:
        ht_prob = poisson_prob(team_a_ht_goal_rate, home_goals) * poisson_prob(team_b_ht_goal_rate, away_goals)
        ht_results.append((home_goals, away_goals, ht_prob))

    # Calculate Poisson probabilities for FT scorelines
    for home_goals, away_goals in ft_scorelines:
        ft_prob = poisson_prob(team_a_ft_goal_rate, home_goals) * poisson_prob(team_b_ft_goal_rate, away_goals)
        ft_results.append((home_goals, away_goals, ft_prob))

    # Calculate the Poisson probability for FT 1-0
    ft_1_0_prob = next((prob for home, away, prob in ft_results if home == 1 and away == 0), 0)
    adjusted_ft_1_0_prob = adjust_for_over_2_5_goals(over_2_5_odds, ft_1_0_prob)

    # Sort results by Poisson probability in descending order (most likely scoreline first)
    ht_results.sort(key=lambda x: x[2], reverse=True)
    ft_results.sort(key=lambda x: x[2], reverse=True)

    # Display results for Halftime predictions
    st.subheader("Most Likely Half-Time Scorelines:")
    for scoreline in ht_results[:7]:  # Display top 5 HT scorelines
        home, away, prob = scoreline
        adjusted_prob = adjust_for_over_2_5_goals(over_2_5_odds, prob)
        st.write(f"HT {home}-{away} with Poisson Probability: {prob * 100:.2f}%, Adjusted for Over 2.5: {adjusted_prob * 100:.2f}%")

    # Display results for Full-Time predictions
    st.subheader("Most Likely Full-Time Scorelines:")
    for scoreline in ft_results[:9]:  # Display top 5 FT scorelines
        home, away, prob = scoreline
        adjusted_prob = adjust_for_over_2_5_goals(over_2_5_odds, prob)
        st.write(f"FT {home}-{away} with Poisson Probability: {prob * 100:.2f}%, Adjusted for Over 2.5: {adjusted_prob * 100:.2f}%")

    # Display FT 1-0 probability and adjusted for Over 2.5 goals
    st.subheader(f"FT 1-0 (Home Team to Score Exactly 1) with Poisson Probability: {ft_1_0_prob * 100:.2f}%, Adjusted for Over 2.5: {adjusted_ft_1_0_prob * 100:.2f}%")

    # Display Final Recommendation for FT 1-0
    st.subheader("Final Recommendation Based on Poisson Probabilities:")
    st.write(f"Recommended Full-Time Scoreline: FT 1-0 (Home Team to Score Exactly 1) with Poisson Probability: {ft_1_0_prob * 100:.2f}%, Adjusted for Over 2.5: {adjusted_ft_1_0_prob * 100:.2f}%")

    # Display Final Recommendation for HT scoreline
    st.subheader("Final Recommendation Based on Half-Time Poisson Probabilities:")
    ht_recommended_score = ht_results[0]
    ht_home, ht_away, ht_prob = ht_recommended_score
    st.write(f"Recommended Half-Time Scoreline: HT {ht_home}-{ht_away} with Poisson Probability: {ht_prob * 100:.2f}%")

# Add a submit button to the sidebar
with st.sidebar:
    st.markdown("### Submit Prediction")
    if st.button("Submit Prediction"):
        st.success("Prediction submitted! Results will be displayed below.")

# Main app
st.title("🤖🤖⚽⚽⚽💯💯💯 Rabiotic Football Match Prediction using Poisson Distribution")
calculate_predictions()
