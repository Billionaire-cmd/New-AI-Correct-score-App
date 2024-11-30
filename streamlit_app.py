import streamlit as st
import numpy as np
from scipy.stats import poisson
import pandas as pd

# Function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate the implied probability from odds
def implied_prob(odds):
    return 1 / odds * 100

# Function to calculate predictions for a single game
def calculate_game_predictions(game_id, home_goals, away_goals, home_conceded, away_conceded):
    home_expected_goals = home_goals * away_conceded
    away_expected_goals = away_goals * home_conceded

    home_goals_dist = poisson(home_expected_goals)
    away_goals_dist = poisson(away_expected_goals)

    correct_score_probs = {}
    for i in range(6):  # Home goals (0-5)
        for j in range(6):  # Away goals (0-5)
            prob = home_goals_dist.pmf(i) * away_goals_dist.pmf(j)
            correct_score_probs[f"{i}-{j}"] = prob * 100  # Convert to percentage

    most_likely_score = max(correct_score_probs, key=correct_score_probs.get)
    most_likely_score_prob = correct_score_probs[most_likely_score]

    return {
        "Game ID": game_id,
        "Most Likely Score": most_likely_score,
        "Probability": most_likely_score_prob,
        "All Probabilities": correct_score_probs,
    }

# Main function for app
def main():
    st.title("Football Game Predictions")
    st.sidebar.header("Game Input")
    num_games = st.sidebar.number_input("Number of Games", min_value=1, value=1)

    game_data = []
    for i in range(num_games):
        st.sidebar.subheader(f"Game {i + 1} Details")
        home_goals = st.sidebar.number_input(f"Game {i + 1} - Home Avg Goals", min_value=0.0, value=1.5, key=f"home_goals_{i}")
        away_goals = st.sidebar.number_input(f"Game {i + 1} - Away Avg Goals", min_value=0.0, value=1.2, key=f"away_goals_{i}")
        home_conceded = st.sidebar.number_input(f"Game {i + 1} - Home Avg Conceded", min_value=0.0, value=1.0, key=f"home_conceded_{i}")
        away_conceded = st.sidebar.number_input(f"Game {i + 1} - Away Avg Conceded", min_value=0.0, value=1.3, key=f"away_conceded_{i}")

        game_data.append({
            "Game ID": f"Game {i + 1}",
            "Home Goals": home_goals,
            "Away Goals": away_goals,
            "Home Conceded": home_conceded,
            "Away Conceded": away_conceded,
        })

    if st.sidebar.button("Calculate Predictions"):
        results = []
        st.header("Predictions")
        for game in game_data:
            prediction = calculate_game_predictions(
                game["Game ID"],
                game["Home Goals"],
                game["Away Goals"],
                game["Home Conceded"],
                game["Away Conceded"],
            )
            results.append(prediction)

            st.subheader(prediction["Game ID"])
            st.write(f"Most Likely Score: **{prediction['Most Likely Score']}** with Probability: **{prediction['Probability']:.2f}%**")
            st.write("Correct Score Probabilities:")
            st.table(pd.DataFrame(prediction["All Probabilities"].items(), columns=["Scoreline", "Probability (%)"]).sort_values(by="Probability (%)", ascending=False))

        # Export results as CSV
        export_data = pd.DataFrame([
            {"Game ID": r["Game ID"], "Most Likely Score": r["Most Likely Score"], "Probability": r["Probability"]}
            for r in results
        ])
        csv = export_data.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results as CSV", data=csv, file_name="football_predictions.csv", mime="text/csv")

if __name__ == "__main__":
    main()
