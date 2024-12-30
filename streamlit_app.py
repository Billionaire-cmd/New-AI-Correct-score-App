# Importing required libraries
import streamlit as st
import numpy as np
from scipy.stats import poisson

# Title
st.title("⚽ Advanced Football Match Probability and Recommendation Predictor")

# Input parameters
st.header("Team Statistics")
st.write("Provide the average goals scored and conceded for each team.")

# Team A (Home) statistics
home_goals_scored = st.number_input("Team A Average Goals Scored at Home (e.g., 1.5)", value=1.5)
away_goals_conceded = st.number_input("Team B Average Goals Conceded Away (e.g., 1.2)", value=1.2)

# Team B (Away) statistics
away_goals_scored = st.number_input("Team B Average Goals Scored Away (e.g., 1.3)", value=1.3)
home_goals_conceded = st.number_input("Team A Average Goals Conceded at Home (e.g., 1.1)", value=1.1)

# Team Form Percentages
st.header("Team Form Percentage")
form_percentage_A = st.number_input("Team A Form Percentage (e.g., 73)", value=73) / 100
form_percentage_B = st.number_input("Team B Form Percentage (e.g., 80)", value=80) / 100

# Odds Information
st.header("Odds Information")
odds_home = st.number_input("Odds for Home Win", value=2.5)
odds_draw = st.number_input("Odds for Draw", value=3.2)
odds_away = st.number_input("Odds for Away Win", value=2.8)

# Calculate expected goals
expected_goals_A = (home_goals_scored + away_goals_conceded) / 2
expected_goals_B = (away_goals_scored + home_goals_conceded) / 2

st.subheader("Expected Goals")
st.write(f"Expected Goals for Team A: **{expected_goals_A:.2f}**")
st.write(f"Expected Goals for Team B: **{expected_goals_B:.2f}**")

# Generate Poisson distribution probabilities for scorelines
def calculate_scoreline_probabilities(max_goals=5):
    """Generate a matrix of probabilities for scorelines."""
    prob_matrix = np.zeros((max_goals, max_goals))
    for i in range(max_goals):
        for j in range(max_goals):
            prob_matrix[i, j] = poisson.pmf(i, expected_goals_A) * poisson.pmf(j, expected_goals_B)
    return prob_matrix

scoreline_probs = calculate_scoreline_probabilities(max_goals=6)  # Limit to 5 goals per team

# Flatten the matrix and sort by probability
scoreline_list = []
for i in range(scoreline_probs.shape[0]):
    for j in range(scoreline_probs.shape[1]):
        scoreline_list.append(((i, j), scoreline_probs[i, j]))

scoreline_list.sort(key=lambda x: x[1], reverse=True)

# Display top 9 most likely scorelines
st.subheader("Top 9 Most Likely Scorelines")
top_9_scorelines = scoreline_list[:9]
for idx, ((home_goals, away_goals), prob) in enumerate(top_9_scorelines):
    st.write(f"{idx + 1}. {home_goals}-{away_goals} with Probability: **{prob * 100:.2f}%**")

# Highlight the 3 most likely scorelines
st.subheader("Top 3 Most Likely Scorelines")
top_3_scorelines = scoreline_list[:3]
for idx, ((home_goals, away_goals), prob) in enumerate(top_3_scorelines):
    st.write(f"{idx + 1}. {home_goals}-{away_goals} with Probability: **{prob * 100:.2f}%**")

# Previous functionalities remain (e.g., Over/Under, 1x2, GG/NG)
# Calculate 1x2 probabilities
win_prob_A = np.sum(scoreline_probs[:scoreline_probs.shape[0], :np.tril_indices(scoreline_probs.shape[1], -1)[1].max()]) * form_percentage_A
draw_prob = np.sum([scoreline_probs[i, i] for i in range(scoreline_probs.shape[0])])
win_prob_B = np.sum(scoreline_probs[:scoreline_probs.shape[0], :np.triu_indices(scoreline_probs.shape[1], 1)[0].max()]) * form_percentage_B

# Over/Under and GG/NG probabilities (for brevity, omitted redundant formulas—refer to earlier code)
ou_probs = {
    "Over 1.5": 1 - (scoreline_probs[0, 0] + scoreline_probs[0, 1] + scoreline_probs[1, 0]),
    "Under 1.5": scoreline_probs[0, 0] + scoreline_probs[0, 1] + scoreline_probs[1, 0],
    "Over 2.5": 1 - np.sum(scoreline_probs[:2, :2]),
    "Under 2.5": np.sum(scoreline_probs[:2, :2]),
    "Over 3.5": 1 - np.sum(scoreline_probs[:3, :3]),
    "Under 3.5": np.sum(scoreline_probs[:3, :3]),
}

gg_prob = 1 - (scoreline_probs[:, 0].sum() + scoreline_probs[0, :].sum() - scoreline_probs[0, 0])
ng_prob = 1 - gg_prob

# Recommendations
st.subheader("Probability-Based Recommendations")
st.write(f"Probability of Home Win: **{win_prob_A:.2%}**")
st.write(f"Probability of Draw: **{draw_prob:.2%}**")
st.write(f"Probability of Away Win: **{win_prob_B:.2%}**")

st.write(f"Recommendation: **{'Home Win' if win_prob_A > max(win_prob_B, draw_prob) else 'Away Win' if win_prob_B > max(win_prob_A, draw_prob) else 'Draw'}**")
st.write(f"Over/Under 2.5 Recommendation: **{'Over' if ou_probs['Over 2.5'] > ou_probs['Under 2.5'] else 'Under'} 2.5 Goals**")
st.write(f"GG/NG Recommendation: **{'GG' if gg_prob > ng_prob else 'NG'}**")
