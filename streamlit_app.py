import streamlit as st
import numpy as np
from scipy.stats import poisson

# Function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate the implied probability from odds
def implied_prob(odds):
    return 1 / odds * 100

# Function to generate all possible scorelines (for both HT and FT)
def generate_scorelines(max_goals=5):
    return [(home_goals, away_goals) for home_goals in range(max_goals + 1) for away_goals in range(max_goals + 1)]

# Main function to calculate predictions and display results
def calculate_predictions():
    st.title("Football Match Prediction: Correct Scores and Probabilities")

    # Input Fields for Team Statistics
    st.subheader("Team Statistics")
    team_a_goals = st.number_input("Team A Average Goals Scored", min_value=0.0, value=1.5)
    team_b_goals = st.number_input("Team B Average Goals Scored", min_value=0.0, value=1.2)
    team_a_conceded = st.number_input("Team A Average Goals Conceded", min_value=0.0, value=1.0)
    team_b_conceded = st.number_input("Team B Average Goals Conceded", min_value=0.0, value=1.1)

    # Input Fields for Odds
    st.sidebar.subheader("Odds Inputs")
    ft_home_odds = st.sidebar.number_input("Full-Time Home Win Odds", min_value=1.0, value=2.5)
    ft_draw_odds = st.sidebar.number_input("Full-Time Draw Odds", min_value=1.0, value=3.2)
    ft_away_odds = st.sidebar.number_input("Full-Time Away Win Odds", min_value=1.0, value=2.8)
    over_2_5_odds = st.sidebar.number_input("Over 2.5 Goals Odds", min_value=1.0, value=1.8)
    under_2_5_odds = st.sidebar.number_input("Under 2.5 Goals Odds", min_value=1.0, value=2.0)

    # Expected Goals Calculation
    home_expected_goals = team_a_goals * team_b_conceded
    away_expected_goals = team_b_goals * team_a_conceded

    # Poisson Distribution
    home_goals_dist = poisson(home_expected_goals)
    away_goals_dist = poisson(away_expected_goals)

    # Generate Scorelines and Calculate Probabilities
    scorelines = generate_scorelines()
    correct_score_probs = {
        f"{home}-{away}": home_goals_dist.pmf(home) * away_goals_dist.pmf(away)
        for home, away in scorelines
    }

    # Most Likely Scorelines
    sorted_scores = sorted(correct_score_probs.items(), key=lambda x: x[1], reverse=True)
    most_likely_score_ft = sorted_scores[0]

    # Outcome Probabilities
    home_win_prob = sum(
        home_goals_dist.pmf(h) * sum(away_goals_dist.pmf(a) for a in range(h))
        for h in range(6)
    ) * 100
    draw_prob = sum(
        home_goals_dist.pmf(h) * away_goals_dist.pmf(h) for h in range(6)
    ) * 100
    away_win_prob = sum(
        away_goals_dist.pmf(a) * sum(home_goals_dist.pmf(h) for h in range(a))
        for a in range(6)
    ) * 100

    over_2_5_prob = sum(
        home_goals_dist.pmf(h) * away_goals_dist.pmf(a)
        for h in range(6) for a in range(6) if h + a > 2
    ) * 100
    under_2_5_prob = 100 - over_2_5_prob

    # BTTS (Both Teams to Score) Probability
    btts_prob = sum(
        home_goals_dist.pmf(h) * away_goals_dist.pmf(a)
        for h in range(1, 6) for a in range(1, 6)
    ) * 100

    # Display Results
    st.subheader("Match Predictions")
    st.write(f"🏠 **Home Win Probability:** {home_win_prob:.2f}%")
    st.write(f"🤝 **Draw Probability:** {draw_prob:.2f}%")
    st.write(f"📈 **Away Win Probability:** {away_win_prob:.2f}%")
    st.write(f"⚽ **Over 2.5 Goals Probability:** {over_2_5_prob:.2f}%")
    st.write(f"❌ **Under 2.5 Goals Probability:** {under_2_5_prob:.2f}%")
    st.write(f"🔄 **BTTS Probability:** {btts_prob:.2f}%")
    st.write(f"**Most Likely Full-Time Score:** {most_likely_score_ft[0]} with Probability: {most_likely_score_ft[1] * 100:.2f}%")

    # Display Top 5 Scorelines
    st.subheader("Top 5 Likely Scorelines")
    for score, prob in sorted_scores[:5]:
        st.write(f"Scoreline {score}: {prob * 100:.2f}%")

# Run the Application
if __name__ == "__main__":
    calculate_predictions()
