# Importing required libraries
import streamlit as st
import numpy as np
import pandas as pd
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

# Generate Poisson distribution probabilities for 0 to 3+ goals
def poisson_prob(expected_goals, max_goals=3):
    """Returns probabilities of scoring 0, 1, 2, 3+ goals."""
    probs = [poisson.pmf(i, expected_goals) for i in range(max_goals)]
    probs.append(1 - sum(probs))  # 3+ goals
    return probs

probs_A = poisson_prob(expected_goals_A)
probs_B = poisson_prob(expected_goals_B)

# Display deep analysis of team goals probabilities
st.subheader("Deep Analysis of Team Goals Probability (%)")
st.write("### Team A (Home)")
for i, prob in enumerate(probs_A):
    st.write(f"Probability of Team A scoring {i if i < 3 else '3+'} goals: **{prob * 100:.2f}%**")

st.write("### Team B (Away)")
for i, prob in enumerate(probs_B):
    st.write(f"Probability of Team B scoring {i if i < 3 else '3+'} goals: **{prob * 100:.2f}%**")

# Calculate 1x2 probabilities
win_prob_A = np.sum(np.tril(probs_A, k=-1)) * form_percentage_A
draw_prob = np.sum(probs_A[i] * probs_B[i] for i in range(len(probs_A)))
win_prob_B = np.sum(np.triu(probs_B, k=1)) * form_percentage_B

# Calculate Over/Under probabilities
ou_probs = {
    "Over 1.5": 1 - (probs_A[0] * probs_B[0] + probs_A[0] * probs_B[1] + probs_A[1] * probs_B[0]),
    "Under 1.5": probs_A[0] * probs_B[0] + probs_A[0] * probs_B[1] + probs_A[1] * probs_B[0],
    "Over 2.5": 1 - (probs_A[0] * probs_B[0] + probs_A[0] * probs_B[1] + probs_A[1] * probs_B[0] + probs_A[1] * probs_B[1]),
    "Under 2.5": probs_A[0] * probs_B[0] + probs_A[0] * probs_B[1] + probs_A[1] * probs_B[0] + probs_A[1] * probs_B[1],
    "Over 3.5": 1 - np.sum(probs_A[:3]) * np.sum(probs_B[:3]),
    "Under 3.5": np.sum(probs_A[:3]) * np.sum(probs_B[:3]),
}

# Calculate GG/NG probabilities
gg_prob = np.sum([probs_A[i] * probs_B[j] for i in range(1, len(probs_A)) for j in range(1, len(probs_B))])
ng_prob = 1 - gg_prob

# Scoreline calculation (Advanced)
scoreline_probs = {}
for i in range(4):  # Possible goals for Team A
    for j in range(4):  # Possible goals for Team B
        scoreline_probs[f"{i}-{j}"] = probs_A[i] * probs_B[j]

# Sort scorelines by probability
sorted_scorelines = sorted(scoreline_probs.items(), key=lambda x: x[1], reverse=True)

# Display top 9 most likely scorelines with probabilities
st.subheader("Top 9 Most Likely Scorelines")
for i, (scoreline, prob) in enumerate(sorted_scorelines[:9]):
    st.write(f"{scoreline}: **{prob * 100:.2f}%**")

# Top 3 most likely scorelines for recommendation
top_3_scorelines = sorted_scorelines[:3]

# Recommendation based on top scorelines
st.subheader("Recommended Scoreline Bet")
for scoreline, prob in top_3_scorelines:
    st.write(f"Recommended Bet on Scoreline **{scoreline}** with probability **{prob * 100:.2f}%**")

# Recommendations
st.subheader("Probability-Based Recommendations")
st.write("### 1x2 Recommendations")
st.write(f"Probability of Home Win: **{win_prob_A:.2%}**")
st.write(f"Probability of Draw: **{draw_prob:.2%}**")
st.write(f"Probability of Away Win: **{win_prob_B:.2%}**")

if win_prob_A > win_prob_B and win_prob_A > draw_prob:
    st.write("Recommendation: Bet on **Home Win**")
elif win_prob_B > win_prob_A and win_prob_B > draw_prob:
    st.write("Recommendation: Bet on **Away Win**")
else:
    st.write("Recommendation: Bet on **Draw**")

st.write("### Over/Under Recommendations")
for key, value in ou_probs.items():
    st.write(f"Probability of {key}: **{value * 100:.2f}%**")
st.write(f"Recommendation: Bet on **{'Over' if ou_probs['Over 2.5'] > 0.5 else 'Under'} 2.5 Goals**")

st.write("### GG/NG Recommendations")
st.write(f"Probability of GG: **{gg_prob:.2%}**")
st.write(f"Probability of NG: **{ng_prob:.2%}**")
st.write(f"Recommendation: Bet on **{'GG' if gg_prob > 0.5 else 'NG'}**")

st.write("### Combined Recommendations (Over/Under 2.5 & GG/NG)")
if ou_probs["Over 2.5"] > 0.5 and gg_prob > 0.5:
    st.write("Recommendation: Bet on **Over 2.5 & GG**")
elif ou_probs["Under 2.5"] > 0.5 and ng_prob > 0.5:
    st.write("Recommendation: Bet on **Under 2.5 & NG**")
else:
    st.write("Recommendation: No clear combination bet value.")
