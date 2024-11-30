import streamlit as st
import numpy as np
from scipy.stats import poisson

# Function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate the implied probability from odds
def implied_prob(odds):
    return 1 / odds * 100

# Function to adjust probabilities for over 2.5 goals
def adjust_for_over_2_5_goals(over_2_5_odds, poisson_prob):
    over_2_5_prob = implied_prob(over_2_5_odds)
    adjusted_prob = poisson_prob * (over_2_5_prob / 100)
    return adjusted_prob

# Generate all possible scorelines (for both HT and FT)
def generate_scorelines(max_goals=5):
    scorelines = [(home_goals, away_goals) for home_goals in range(max_goals + 1) for away_goals in range(max_goals + 1)]
    return scorelines

# Main function to calculate and display predictions
def calculate_predictions():
    # Team A and Team B Stats
    team_a_home_goals = st.number_input("Team A Average Goals Scored (Home)", min_value=0.0, value=3.0)
    team_b_away_goals = st.number_input("Team B Average Goals Scored (Away)", min_value=0.0, value=1.29)
    team_a_home_conceded = st.number_input("Team A Average Goals Conceded (Home)", min_value=0.0, value=1.00)                                                                                                 
    team_b_away_conceded = st.number_input("Team B Average Goals Conceded (Away)", min_value=0.0, value=1.79)

    # Sidebar Inputs for Odds
    st.sidebar.subheader("Odds Inputs")
    ht_home_odds = st.sidebar.number_input("HT Home Odds", min_value=0.0, value=1.47)
    ht_draw_odds = st.sidebar.number_input("HT Draw Odds", min_value=0.0, value=3.50)
    ht_away_odds = st.sidebar.number_input("HT Away Odds", min_value=0.0, value=10.50)
    ft_home_odds = st.sidebar.number_input("FT Home Odds", min_value=0.0, value=1.17)
    ft_draw_odds = st.sidebar.number_input("FT Draw Odds", min_value=0.0, value=9.70)
    ft_away_odds = st.sidebar.number_input("FT Away Odds", min_value=0.0, value=16.50)
    over_2_5_odds = st.number_input("Over 2.5 Goals Odds", min_value=1.0, value=1.29)
    under_2_5_odds = st.number_input("Under 2.5 Goals Odds", min_value=1.0, value=4.10)

    # Sidebar Inputs for BTTS (GG/NG) Odds
    st.sidebar.subheader("BTTS (GG/NG) Odds")
    btts_gg_odds = st.sidebar.number_input("BTTS GG Odds", min_value=1.0, value=1.82)
    btts_ng_odds = st.sidebar.number_input("BTTS NG Odds", min_value=1.0, value=2.00)

    st.sidebar.header("Team Strengths")
    home_attack = st.sidebar.number_input("Home Attack Strength", value=2.39, format="%.2f")
    home_defense = st.sidebar.number_input("Home Defense Strength", value=0.56, format="%.2f")
    away_attack = st.sidebar.number_input("Away Attack Strength", value=1.20, format="%.f")
    away_defense = st.sidebar.number_input("Away Defense Strength", value=1.33, format="%.f")

    # Submit Button
    if st.sidebar.button("Submit Prediction"):
        st.success("Prediction submitted! Results will be displayed below.")

        # Expected Goals Calculation
        home_expected_goals = st.sidebar.number_input("Home Team Expected Goals", value=1.36, format="%.2f")
        away_expected_goals = st.sidebar.number_input("Away Team Expected Goals", value=2.96, format="%.1f")

        # Poisson Distributions for Full-time
        home_goals_dist = poisson(home_expected_goals)
        away_goals_dist = poisson(away_expected_goals)

        # Poisson Distributions for Halftime (assuming half the expected goals for each team)
        home_goals_dist_ht = poisson(home_expected_goals / 2)
        away_goals_dist_ht = poisson(away_expected_goals / 3)

        # Correct Score Probabilities for Full-time
        correct_score_probs_ft = {}
        for i in range(6):  # Home goals (0-5)
            for j in range(6):  # Away goals (0-5)
                prob = home_goals_dist.pmf(i) * away_goals_dist.pmf(j)
                correct_score_probs_ft[f"{i}-{j}"] = prob

        # Correct Score Probabilities for Halftime
        correct_score_probs_ht = {}
        for i in range(6):  # Home goals (0-5)
            for j in range(6):  # Away goals (0-5)
                prob = home_goals_dist_ht.pmf(i) * away_goals_dist_ht.pmf(j)
                correct_score_probs_ht[f"{i}-{j}"] = prob

        # Most Likely Scoreline Full-time
        most_likely_scoreline_ft = max(correct_score_probs_ft, key=correct_score_probs_ft.get)
        most_likely_scoreline_prob_ft = correct_score_probs_ft[most_likely_scoreline_ft] * 100

        # Most Likely Scoreline Halftime
        most_likely_scoreline_ht = max(correct_score_probs_ht, key=correct_score_probs_ht.get)
        most_likely_scoreline_prob_ht = correct_score_probs_ht[most_likely_scoreline_ht] * 100

        # Multi-Scoreline Correct Score Probabilities (Top 3)
        sorted_ht_probs = sorted(correct_score_probs_ht.items(), key=lambda x: x[1], reverse=True)[:3]
        sorted_ft_probs = sorted(correct_score_probs_ft.items(), key=lambda x: x[1], reverse=True)[:3]

        # Probabilities for Outcomes
        home_win_prob = sum(
            home_goals_dist.pmf(i) * sum(away_goals_dist.pmf(j) for j in range(i))
            for i in range(6)
        ) * 100

        draw_prob = sum(
            home_goals_dist.pmf(i) * away_goals_dist.pmf(i) for i in range(6)
        ) * 100

        away_win_prob = sum(
            away_goals_dist.pmf(i) * sum(home_goals_dist.pmf(j) for j in range(i))
            for i in range(6)
        ) * 100

        over_2_5_prob = sum(
            home_goals_dist.pmf(i) * away_goals_dist.pmf(j)
            for i in range(6) for j in range(6) if i + j > 2
        ) * 100
        under_2_5_prob = 100 - over_2_5_prob

        # BTTS Probability
        btts_prob = sum(
            home_goals_dist.pmf(i) * away_goals_dist.pmf(j)
            for i in range(1, 6) for j in range(1, 6)
        ) * 100

        # BTTS GG/NG ODDS Calculation
        btts_gg_prob = implied_prob(btts_gg_odds)
        btts_ng_prob = implied_prob(btts_ng_odds)

        # HT/FT Probabilities
        ht_ft_probs = {
            "1/1": home_win_prob / 3, "1/X": draw_prob / 3, "1/2": away_win_prob / 3,
            "X/1": home_win_prob / 1, "X/X": draw_prob / 2, "X/2": away_win_prob / 2,
            "2/1": home_win_prob / 3, "2/X": draw_prob / 3, "2/2": away_win_prob / 3
        }

        # Display Outputs
        st.subheader("Predicted Probabilities")
        st.write(f"🏠 **Home Win Probability:** {home_win_prob:.2f}%")
        st.write(f"🤝 **Draw Probability:** {draw_prob:.2f}%")
        st.write(f"📈 **Away Win Probability:** {away_win_prob:.2f}%")
        st.write(f"⚽ **Over 2.5 Goals Probability:** {over_2_5_prob:.2f}%")
        st.write(f"❌ **Under 2.5 Goals Probability:** {under_2_5_prob:.3f}%")
        st.write(f"🔄 **BTTS Probability (Yes):** {btts_prob:.5f}%")
        
        st.write(f"**Most Likely Halftime Correct Score:** {most_likely_scoreline_ht} - Probability: {most_likely_scoreline_prob_ht:.2f}%")
        st.write(f"**Most Likely Full-time Correct Score:** {most_likely_scoreline_ft} - Probability: {most_likely_scoreline_prob_ft:.2f}%")
        
        # Multi-Scoreline
        st.write("**Top 3 Halftime Correct Score Multi-Scoreline Probabilities**")
        for scoreline, prob in sorted_ht_probs:
            st.write(f"{scoreline}: {prob:.2f}%")

        st.write("**Top 3 Full-time Correct Score Multi-Scoreline Probabilities**")
        for scoreline, prob in sorted_ft_probs:
            st.write(f"{scoreline}: {prob:.2f}%")

        # HT/FT Predictions
        st.write("**HT/FT Probabilities**")
        for outcome, prob in ht_ft_probs.items():
            st.write(f"{outcome}: {prob:.2f}%")

# Call the function to run the calculations
calculate_predictions()
