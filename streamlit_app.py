import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson

# Title
st.title("🤖🤖🤖⚽💯💯💯Rabiotic Football Match Real Correct Score Predictor")

# Input parameters
st.header("Team Statistics")
avg_goals_A = st.number_input("Average Goals Scored by Team A (e.g., 1.3)", value=1.3)
avg_goals_B = st.number_input("Average Goals Scored by Team B (e.g., 1.7)", value=1.7)
form_percentage_A = st.number_input("Team A Form Percentage (e.g., 75)", value=75.0)
form_percentage_B = st.number_input("Team B Form Percentage (e.g., 70)", value=70.0)
max_goals = st.slider("Maximum Goals to Consider (e.g., 5)", min_value=1, max_value=10, value=5)

# Previous meetings
st.header("Previous Meeting Results")
home_wins = st.number_input("Home Wins (e.g., Team A wins at home)", value=2)
draws = st.number_input("Draws (e.g., Previous draws between the teams)", value=1)
away_wins = st.number_input("Away Wins (e.g., Team B wins away)", value=3)

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

# Calculate team performance weights
total_meetings = home_wins + draws + away_wins
if total_meetings > 0:
    home_win_weight = home_wins / total_meetings
    draw_weight = draws / total_meetings
    away_win_weight = away_wins / total_meetings
else:
    home_win_weight = draw_weight = away_win_weight = 0

# Generate Poisson matrix
st.subheader("Prediction Matrix")
score_matrix = np.zeros((max_goals + 1, max_goals + 1))
for i in range(max_goals + 1):
    for j in range(max_goals + 1):
        score_matrix[i, j] = (
            poisson.pmf(i, avg_goals_A) * poisson.pmf(j, avg_goals_B)
        )

# Adjust matrix with form percentage and previous meeting weights
adjustment_factor = (form_percentage_A / 100) * home_win_weight + \
                    (form_percentage_B / 100) * away_win_weight + \
                    draw_weight
score_matrix *= adjustment_factor

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

# Outcome probabilities
st.subheader("Outcome Probabilities")
win_prob_A = np.sum(np.tril(score_matrix, k=-1))  # Team A wins
draw_prob = np.sum(np.diag(score_matrix))        # Draw
win_prob_B = np.sum(np.triu(score_matrix, k=1))  # Team B wins

st.write(f"Probability of Home Win: **{win_prob_A:.2%}**")
st.write(f"Probability of Draw: **{draw_prob:.2%}**")
st.write(f"Probability of Away Win: **{win_prob_B:.2%}**")

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

# Value bet analysis
st.subheader("Value Bet Analysis")
ev_home = (win_prob_A * odds_home) - 1
ev_draw = (draw_prob * odds_draw) - 1
ev_away = (win_prob_B * odds_away) - 1

st.write(f"Expected Value for Home Win: **{ev_home:.2f}**")
st.write(f"Expected Value for Draw: **{ev_draw:.2f}**")
st.write(f"Expected Value for Away Win: **{ev_away:.2f}**")

# Final recommendation
st.subheader("Final Recommendation")
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

final_recommendation = "No clear value bet detected."
if ev_home > 0:
    likely_score = get_most_likely_score("home_win")
    if likely_score:
        final_recommendation = f"Value Bet Recommendation: **Home Win** with Correct Score **{likely_score[0]}-{likely_score[1]}**"
elif ev_draw > 0:
    likely_score = get_most_likely_score("draw")
    if likely_score:
        final_recommendation = f"Value Bet Recommendation: **Draw** with Correct Score **{likely_score[0]}-{likely_score[1]}**"
elif ev_away > 0:
    likely_score = get_most_likely_score("away_win")
    if likely_score:
        final_recommendation = f"Value Bet Recommendation: **Away Win** with Correct Score **{likely_score[0]}-{likely_score[1]}**"

st.write(final_recommendation)
