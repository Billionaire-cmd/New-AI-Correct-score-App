import streamlit as st
import numpy as np
from scipy.stats import poisson

# Set page title
st.set_page_config(page_title="Football Match Correct Score Predictor", layout="wide")

# App title
st.title("🤖🤖🤖💯Rabiotic Football Match Correct Score Predictor")
st.write("This app predicts correct scores and provides detailed insights using statistics, league table data, and odds.")

# Input form
st.sidebar.header("Input Match Details")
team_a = st.sidebar.text_input("Team A", value="Team A")
team_b = st.sidebar.text_input("Team B", value="Team B")

# League statistics
matches_played_a = st.sidebar.number_input("Matches Played by Team A", min_value=0, value=10)
matches_played_b = st.sidebar.number_input("Matches Played by Team B", min_value=0, value=10)
wins_a = st.sidebar.number_input("Wins by Team A", min_value=0, value=5)
wins_b = st.sidebar.number_input("Wins by Team B", min_value=0, value=6)
draws_a = st.sidebar.number_input("Draws by Team A", min_value=0, value=3)
draws_b = st.sidebar.number_input("Draws by Team B", min_value=0, value=2)
losses_a = st.sidebar.number_input("Losses by Team A", min_value=0, value=2)
losses_b = st.sidebar.number_input("Losses by Team B", min_value=0, value=2)
goal_diff_a = st.sidebar.number_input("Goal Difference of Team A", value=10)
goal_diff_b = st.sidebar.number_input("Goal Difference of Team B", value=8)
points_a = st.sidebar.number_input("Points of Team A", value=18)
points_b = st.sidebar.number_input("Points of Team B", value=20)

# Additional statistics
avg_goals_a = st.sidebar.number_input("Average Goals Scored by Team A", min_value=0.0, value=1.5)
avg_goals_b = st.sidebar.number_input("Average Goals Scored by Team B", min_value=0.0, value=1.8)
form_a = st.sidebar.slider("Form Percentage of Team A", min_value=0, max_value=100, value=80)
form_b = st.sidebar.slider("Form Percentage of Team B", min_value=0, max_value=100, value=20)

# Full-time odds
home_odds = st.sidebar.number_input("Full-Time Odds (Home Win)", min_value=1.0, value=2.5)
draw_odds = st.sidebar.number_input("Full-Time Odds (Draw)", min_value=1.0, value=3.0)
away_odds = st.sidebar.number_input("Full-Time Odds (Away Win)", min_value=1.0, value=2.8)

# Add a submit button to the sidebar
with st.sidebar:
    st.markdown("### Submit Prediction")
    if st.button("Submit Prediction"):
        st.success("Prediction submitted! Results will be displayed below.")

# Calculate attack and defense strengths
attack_strength_a = avg_goals_a * (form_a / 50)
attack_strength_b = avg_goals_b * (form_b / 40)

# Generate Poisson distribution probabilities
max_goals = 5
team_a_probs = [poisson.pmf(i, attack_strength_a) for i in range(max_goals + 2)]
team_b_probs = [poisson.pmf(i, attack_strength_b) for i in range(max_goals + 2)]

# Generate probability matrix
prob_matrix = np.outer(team_a_probs, team_b_probs)

# Calculate outcome probabilities
home_win_prob = np.sum([prob_matrix[i, j] for i in range(max_goals - 2) for j in range(max_goals - 1) if i > j])
draw_prob = np.sum([prob_matrix[i, j] for i in range(max_goals - 2) for j in range(max_goals - 1) if i < j])
away_win_prob = np.sum([prob_matrix[i, j] for i in range(max_goals - 2) for j in range(max_goals - 1) if i == j])

# Weight probabilities by odds
weighted_home_win_prob = home_win_prob / home_odds
weighted_draw_prob = draw_prob / draw_odds
weighted_away_win_prob = away_win_prob / away_odds

# Normalize probabilities
total_prob = weighted_home_win_prob + weighted_draw_prob + weighted_away_win_prob
home_win_percentage = (weighted_home_win_prob / total_prob) * 100
draw_percentage = (weighted_draw_prob / total_prob) * 100
away_win_percentage = (weighted_away_win_prob / total_prob) * 100

# Most likely outcome
most_likely_outcome = max(
    ("Home Win", home_win_percentage),
    ("Draw", draw_percentage),
    ("Away Win", away_win_percentage),
    key=lambda x: x[1],
)

# Recommended correct score based on the most likely outcome
if most_likely_outcome[0] == "Home Win":
    recommended_score = max(
        [(i, j, prob_matrix[i, j]) for i in range(max_goals + 1) for j in range(i)],
        key=lambda x: x[2],
    )
elif most_likely_outcome[0] == "Draw":
    recommended_score = max(
        [(i, i, prob_matrix[i, i]) for i in range(max_goals + 1)],
        key=lambda x: x[2],
    )
else:  # Away Win
    recommended_score = max(
        [(i, j, prob_matrix[i, j]) for i in range(max_goals + 1) for j in range(i - 1, max_goals + 1)],
        key=lambda x: x[2],
    )

# Display match details
st.write("### Match Details")
st.write(f"**{team_a} vs {team_b}**")
st.write(f"- **Team A Form (%):** {form_a}")
st.write(f"- **Team B Form (%):** {form_b}")
st.write(f"- **Odds (Home - Draw - Away):** {home_odds} - {draw_odds} - {away_odds}")

# Display probabilities
st.write("### Match Outcome Probabilities")
st.write(f"- **Probability of Home Win**: {home_win_percentage:.2f}%")
st.write(f"- **Probability of Draw**: {draw_percentage:.2f}%")
st.write(f"- **Probability of Away Win**: {away_win_percentage:.2f}%")
st.write(f"- **Most Likely Outcome**: {most_likely_outcome[0]} ({most_likely_outcome[1]:.2f}%)")

# Correct scores
st.write("### Correct Score Probabilities")
for i in range(max_goals + 1):
    for j in range(max_goals + 1):
        st.write(f"{team_a} {i} - {team_b} {j}: {prob_matrix[i, j] * 100:.2f}%")

# Recommended correct score
st.write("### Recommended Correct Score")
st.write(f"The recommended correct score is **{team_a} {recommended_score[0]} - {team_b} {recommended_score[1]}** with a probability of **{recommended_score[2] * 100:.2f}%**.")

# Align scores with full-time probabilities
st.write("### Aligned Scores with Outcomes")
st.write("**Home Win Scores:**")
for i in range(max_goals - 2):
    for j in range(i):
        st.write(f"{team_a} {i} - {team_b} {j}: {prob_matrix[i, j] * 100:.2f}%")

st.write("**Draw Scores:**")
for i in range(max_goals - 2):
    st.write(f"{team_a} {i} - {team_b} {i}: {prob_matrix[i, i] * 100:.2f}%")

st.write("**Away Win Scores:**")
for i in range(max_goals - 2):
    for j in range(i - 1, max_goals + 1):
        st.write(f"{team_a} {i} - {team_b} {j}: {prob_matrix[i, j] * 100:.2f}%")
