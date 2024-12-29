# Importing required libraries
import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson

# Title
st.title("🤖🤖🤖💯Rabiotic Football Match Real Correct Score Predictor")

# Input parameters
st.header("Team Statistics")
avg_goals_A = st.number_input("Average Goals Scored by Team A (e.g., 1.3)", value=1.3)
avg_goals_B = st.number_input("Average Goals Scored by Team B (e.g., 1.7)", value=1.7)
max_goals = st.slider("Maximum Goals to Consider (e.g., 5)", min_value=1, max_value=10, value=5)

# Team Form Percentages
st.header("Team Form Percentage")
form_percentage_A = st.number_input("Team A Form Percentage (e.g., 73)", value=73) / 100
form_percentage_B = st.number_input("Team B Form Percentage (e.g., 80)", value=80) / 100

# Previous Meetings
st.header("Previous Meetings")
home_wins = st.number_input("Number of Home Wins for Team A (e.g., 3)", value=3)
draws = st.number_input("Number of Draws in Previous Meetings (e.g., 2)", value=2)
away_wins = st.number_input("Number of Away Wins for Team B (e.g., 4)", value=4)

# Odds Information
st.header("Odds Information")
odds_home = st.number_input("Odds for Home Win", value=2.5)
odds_draw = st.number_input("Odds for Draw", value=3.2)
odds_away = st.number_input("Odds for Away Win", value=2.8)
odds_over_1_5 = st.number_input("Odds for Over 1.5 Goals", value=1.5)
odds_under_1_5 = st.number_input("Odds for Under 1.5 Goals", value=2.6)
odds_over_2_5 = st.number_input("Odds for Over 2.5 Goals", value=1.9)
odds_under_2_5 = st.number_input("Odds for Under 2.5 Goals", value=1.8)
odds_btts_gg = st.number_input("Odds for Both Teams to Score (GG)", value=1.8)
odds_btts_ng = st.number_input("Odds for Both Teams Not to Score (NG)", value=2.0)

# Add a submit button to the sidebar
with st.sidebar:
    st.markdown("### Submit Prediction")
    if st.button("Submit Prediction"):
        st.success("Prediction submitted! Results will be displayed below.")

# Calculate weights for validation
total_meetings = home_wins + draws + away_wins
home_win_prob = home_wins / total_meetings if total_meetings > 0 else 0
draw_prob = draws / total_meetings if total_meetings > 0 else 0
away_win_prob = away_wins / total_meetings if total_meetings > 0 else 0

# Generate Poisson matrix
st.subheader("Prediction Matrix")
score_matrix = np.zeros((max_goals + 1, max_goals + 1))
for i in range(max_goals + 1):
    for j in range(max_goals + 1):
        score_matrix[i, j] = (
            poisson.pmf(i, avg_goals_A) * poisson.pmf(j, avg_goals_B)
            * form_percentage_A * form_percentage_B
        )

# Display the matrix
df_matrix = pd.DataFrame(score_matrix, 
                         index=[f"A: {i}" for i in range(max_goals + 1)], 
                         columns=[f"B: {j}" for j in range(max_goals + 1)])
st.dataframe(df_matrix.style.format("{:.4f}"))

# Most likely scoreline
most_likely_score = np.unravel_index(np.argmax(score_matrix), score_matrix.shape)
most_likely_probability = score_matrix[most_likely_score]

# Results
st.subheader("Results")
st.write(f"The most likely scoreline is **{most_likely_score[0]}-{most_likely_score[1]}** "
         f"with a probability of **{most_likely_probability:.2%}**.")

# Calculate outcome probabilities
win_prob_A = np.sum(np.tril(score_matrix, k=-1))
draw_prob = np.sum(np.diag(score_matrix))
win_prob_B = np.sum(np.triu(score_matrix, k=1))

prob_over_1_5 = np.sum(score_matrix[2:].sum(axis=1) + score_matrix[:, 2:].sum(axis=0)) - score_matrix[2:, 2:].sum()
prob_under_1_5 = 1 - prob_over_1_5
prob_over_2_5 = np.sum(score_matrix[3:].sum(axis=1) + score_matrix[:, 3:].sum(axis=0)) - score_matrix[3:, 3:].sum()
prob_under_2_5 = 1 - prob_over_2_5
prob_btts_gg = np.sum(score_matrix[1:, 1:])
prob_btts_ng = 1 - prob_btts_gg

# Display outcome probabilities
st.subheader("Outcome Probabilities")
st.write(f"Probability of Home Win: **{win_prob_A:.2%}**")
st.write(f"Probability of Draw: **{draw_prob:.2%}**")
st.write(f"Probability of Away Win: **{win_prob_B:.2%}**")
st.write(f"Probability of Over 1.5 Goals: **{prob_over_1_5:.2%}**")
st.write(f"Probability of Under 1.5 Goals: **{prob_under_1_5:.2%}**")
st.write(f"Probability of Over 2.5 Goals: **{prob_over_2_5:.2%}**")
st.write(f"Probability of Under 2.5 Goals: **{prob_under_2_5:.2%}**")
st.write(f"Probability of Both Teams to Score (GG): **{prob_btts_gg:.2%}**")
st.write(f"Probability of Both Teams Not to Score (NG): **{prob_btts_ng:.2%}**")

# Correct score analysis
st.subheader("Correct Score Analysis")
flat_scores = [
    (i, j, score_matrix[i, j]) for i in range(max_goals + 1) for j in range(max_goals + 1)
]
flat_scores.sort(key=lambda x: x[2], reverse=True)

# Display top 5 most likely scores
st.write("### Top 5 Most Likely Scorelines:")
for rank, (i, j, prob) in enumerate(flat_scores[:5], 1):
    st.write(f"{rank}. **{i}-{j}** with probability **{prob:.2%}**")

# Final Recommendation
st.subheader("Final Recommendation")

# Adjust probabilities using odds and team form percentages
adjusted_win_prob_A = win_prob_A * (1 / odds_home) * form_percentage_A
adjusted_draw_prob = draw_prob * (1 / odds_draw)
adjusted_win_prob_B = win_prob_B * (1 / odds_away) * form_percentage_B

def get_most_likely_score(condition):
    filtered_scores = {
        "home_win": [(i, j, score_matrix[i, j]) for i in range(max_goals + 1) for j in range(max_goals + 1) if i > j],
        "draw": [(i, j, score_matrix[i, j]) for i in range(max_goals + 1) for j in range(max_goals + 1) if i == j],
        "away_win": [(i, j, score_matrix[i, j]) for i in range(max_goals + 1) for j in range(max_goals + 1) if i < j],
    }
    scores = filtered_scores[condition]
    if scores:
        return max(scores, key=lambda x: x[2])[:2]
    else:
        return None

# Determine the final recommendation
final_recommendation = "No clear value bet detected."
if adjusted_win_prob_A > adjusted_draw_prob and adjusted_win_prob_A > adjusted_win_prob_B:
    likely_score = get_most_likely_score("home_win")
    if likely_score:
        final_recommendation = f"Value Bet Recommendation: **Home Win** with Correct Score **{likely_score[0]}-{likely_score[1]}**"
elif adjusted_draw_prob > adjusted_win_prob_A and adjusted_draw_prob > adjusted_win_prob_B:
    likely_score = get_most_likely_score("draw")
    if likely_score:
        final_recommendation = f"Value Bet Recommendation: **Draw** with Correct Score **{likely_score[0]}-{likely_score[1]}**"
elif adjusted_win_prob_B > adjusted_win_prob_A and adjusted_win_prob_B > adjusted_draw_prob:
    likely_score = get_most_likely_score("away_win")
    if likely_score:
        final_recommendation = f"Value Bet Recommendation: **Away Win** with Correct Score **{likely_score[0]}-{likely_score[1]}**"

# Display the final recommendation
st.write(final_recommendation)
