import streamlit as st
from scipy.stats import poisson
import matplotlib.pyplot as plt
import numpy as np

# Function to calculate expected goals
def calculate_expected_goals(attack_strength, defense_strength, league_avg_goals):
    return attack_strength * defense_strength * league_avg_goals

# Function to generate Poisson distribution
def generate_poisson_distribution(expected_goals, max_goals=5):
    return [poisson.pmf(i, expected_goals) for i in range(max_goals + 1)]

# Main function to handle the Streamlit app logic
def main():
    st.title('Rabiotic Football Match Prediction ⚽')

    st.sidebar.header('Match Settings')
    
    # Input fields
    home_attack_strength = st.sidebar.number_input("Home Team Attack Strength", min_value=0.1, value=1.2)
    away_defense_strength = st.sidebar.number_input("Away Team Defense Strength", min_value=0.1, value=0.9)
    league_avg_goals = st.sidebar.number_input("League Average Goals per Match", min_value=0.1, value=1.4)
    
    st.sidebar.markdown("### Prediction Output Range")
    max_goals = st.sidebar.slider("Max Goals for Prediction", min_value=3, max_value=10, value=5)

    # Calculate expected goals for home and away teams
    home_expected_goals = calculate_expected_goals(home_attack_strength, away_defense_strength, league_avg_goals)
    away_expected_goals = calculate_expected_goals(away_defense_strength, home_attack_strength, league_avg_goals)
    
    st.subheader("Match Prediction Results")
    st.write(f"Home Expected Goals: {home_expected_goals:.2f}")
    st.write(f"Away Expected Goals: {away_expected_goals:.2f}")
    
    # Generate Poisson distribution for both teams
    home_goals_probabilities = generate_poisson_distribution(home_expected_goals, max_goals)
    away_goals_probabilities = generate_poisson_distribution(away_expected_goals, max_goals)

    # Display the probabilities in a table
    st.write("### Probability Distribution of Goals Scored (Poisson Distribution)")
    
    # Table for home goals probabilities
    home_goals = list(range(max_goals + 1))
    st.write(f"#### Home Goals Probabilities (Mean: {home_expected_goals:.2f})")
    home_goal_probs = list(zip(home_goals, home_goals_probabilities))
    st.write(pd.DataFrame(home_goal_probs, columns=["Goals", "Probability"]))

    # Table for away goals probabilities
    st.write(f"#### Away Goals Probabilities (Mean: {away_expected_goals:.2f})")
    away_goal_probs = list(zip(home_goals, away_goals_probabilities))
    st.write(pd.DataFrame(away_goal_probs, columns=["Goals", "Probability"]))
    
    # Visualization of the goal probabilities
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot Home Goals Probability
    ax.bar(home_goals, home_goals_probabilities, width=0.4, label="Home Goals", align='center', color='b', alpha=0.6)
    
    # Plot Away Goals Probability
    ax.bar(home_goals, away_goals_probabilities, width=0.4, label="Away Goals", align='edge', color='r', alpha=0.6)
    
    ax.set_xlabel('Goals Scored')
    ax.set_ylabel('Probability')
    ax.set_title(f'Goal Scoring Probabilities (Home vs Away)')
    ax.legend()

    # Display the plot
    st.pyplot(fig)
    
    # Predict the most likely scoreline (HT/FT)
    st.write("### Predicted Match Scorelines (Most Likely Outcome)")
    scorelines = [(home_goals[i], home_goals[j]) for i in range(len(home_goals)) for j in range(len(home_goals))]
    score_probabilities = [
        home_goals_probabilities[i] * away_goals_probabilities[j]
        for i in range(len(home_goals)) for j in range(len(home_goals))
    ]
    
    score_probabilities_sum = sum(score_probabilities)
    score_probabilities_normalized = [p / score_probabilities_sum for p in score_probabilities]
    
    scoreline_probs = list(zip(scorelines, score_probabilities_normalized))
    
    # Display the top 5 most probable scorelines
    sorted_scoreline_probs = sorted(scoreline_probs, key=lambda x: x[1], reverse=True)[:5]
    
    st.write("### Top 5 Most Likely Scorelines")
    st.write(pd.DataFrame(sorted_scoreline_probs, columns=["Scoreline (Home-Away)", "Probability"]))

# Run the app
if __name__ == "__main__":
    main()
