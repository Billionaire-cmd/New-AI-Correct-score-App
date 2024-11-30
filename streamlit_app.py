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
    team_a_home_goals = st.number_input("Team A Average Goals Scored (Home)", min_value=0.0, value=0.30)
    team_b_away_goals = st.number_input("Team B Average Goals Scored (Away)", min_value=0.0, value=1.00)
    team_a_home_conceded = st.number_input("Team A Average Goals Conceded (Home)", min_value=0.0, value=1.50)
    team_b_away_conceded = st.number_input("Team B Average Goals Conceded (Away)", min_value=0.0, value=2.00)

    # Sidebar Inputs for Odds
    st.sidebar.subheader("Odds Inputs")
    ht_home_odds = st.sidebar.number_input("HT Home Odds", min_value=0.0, value=4.10)
    ht_draw_odds = st.sidebar.number_input("HT Draw Odds", min_value=0.0, value=2.25)
    ht_away_odds = st.sidebar.number_input("HT Away Odds", min_value=0.0, value=2.70)
    ft_home_odds = st.sidebar.number_input("FT Home Odds", min_value=0.0, value=3.50)
    ft_draw_odds = st.sidebar.number_input("FT Draw Odds", min_value=0.0, value=3.70)
    ft_away_odds = st.sidebar.number_input("FT Away Odds", min_value=0.0, value=2.14)
    over_2_5_odds = st.number_input("Over 2.5 Goals Odds", min_value=1.0, value=1.92)
    under_2_5_odds = st.number_input("Under 2.5 Goals Odds", min_value=1.0, value=1.90)

    # Sidebar Inputs for BTTS (GG/NG) Odds
    st.sidebar.subheader("BTTS (GG/NG) Odds")
    btts_gg_odds = st.sidebar.number_input("BTTS GG Odds", min_value=1.0, value=1.80)
    btts_ng_odds = st.sidebar.number_input("BTTS NG Odds", min_value=1.0, value=2.00)

    st.sidebar.header("Team Strengths")
    home_attack = st.sidebar.number_input("Home Attack Strength", value=1.00, format="%.2f")
    home_defense = st.sidebar.number_input("Home Defense Strength", value=0.80, format="%.2f")
    away_attack = st.sidebar.number_input("Away Attack Strength", value=0.80, format="%.2f")
    away_defense = st.sidebar.number_input("Away Defense Strength", value=0.87, format="%.2f")

    # Submit Button
    if st.sidebar.button("Submit Prediction"):
        st.success("Prediction submitted! Results will be displayed below.")

        # Expected Goals Calculation
        home_expected_goals = st.sidebar.number_input("Home Team Expected Goals", value=1.30, format="%.2f")
        away_expected_goals = st.sidebar.number_input("Away Team Expected Goals", value=0.96, format="%.2f")

        # Poisson Distributions
        home_goals_dist = poisson(home_expected_goals)
        away_goals_dist = poisson(away_expected_goals)

        # Correct Score Probabilities
        correct_score_probs = {}
        for i in range(6):  # Home goals (0-5)
            for j in range(6):  # Away goals (0-5)
                prob = home_goals_dist.pmf(i) * away_goals_dist.pmf(j)
                correct_score_probs[f"{i}-{j}"] = prob

        # Most Likely Scoreline
        most_likely_scoreline = max(correct_score_probs, key=correct_score_probs.get)
        most_likely_scoreline_prob = correct_score_probs[most_likely_scoreline] * 100

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
            "1/1": home_win_prob / 2, "1/X": draw_prob / 2, "1/2": away_win_prob / 2,
            "X/1": home_win_prob / 2, "X/X": draw_prob / 2, "X/2": away_win_prob / 2,
            "2/1": home_win_prob / 2, "2/X": draw_prob / 2, "2/2": away_win_prob / 2
        }

        # Display Outputs
        st.subheader("Predicted Probabilities")
        st.write(f"🏠 **Home Win Probability:** {home_win_prob:.2f}%")
        st.write(f"🤝 **Draw Probability:** {draw_prob:.2f}%")
        st.write(f"📈 **Away Win Probability:** {away_win_prob:.2f}%")
        st.write(f"⚽ **Over 2.5 Goals Probability:** {over_2_5_prob:.2f}%")
        st.write(f"❌ **Under 2.5 Goals Probability:** {under_2_5_prob:.2f}%")
        st.write(f"🔄 **BTTS Probability (Yes):** {btts_prob:.2f}%")
        
        # BTTS GG/NG Odds Recommendation
        st.write(f"**BTTS GG Odds Implied Probability:** {btts_gg_prob:.2f}%")
        st.write(f"**BTTS NG Odds Implied Probability:** {btts_ng_prob:.2f}%")

        # BTTS Recommendation
        if btts_prob >= 50:
            st.write("🔔 **Recommendation: Both Teams to Score (BTTS) is likely!**")
        else:
            st.write("🚫 **Recommendation: BTTS is unlikely!**")

        # Over 2.5 Goals Recommendation
        if over_2_5_prob >= 50:
            st.write("🔔🔔 **Recommendation: Over 2.5 Goals is likely!**")
        else:
            st.write("🚫 **Recommendation: Under 2.5 Goals is likely!**")

        st.subheader("HT/FT Probabilities")
        for ht_ft, prob in ht_ft_probs.items():
            st.write(f"{ht_ft}: {prob:.2f}%")

        st.subheader("Correct Score Probabilities")
        for score, prob in sorted(correct_score_probs.items(), key=lambda x: x[1], reverse=True)[:10]:
            st.write(f"{score}: {prob * 100:.2f}%")

        st.subheader("Most Likely Outcome")
        st.write(f"**The most likely scoreline is {most_likely_scoreline}** with a probability of {most_likely_scoreline_prob:.2f}%")

# Call the function to run the calculations
calculate_predictions()
