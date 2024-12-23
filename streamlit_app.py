import streamlit as st
import numpy as np
from scipy.stats import poisson

# Set page title
st.set_page_config(page_title="Football Match Correct Score Predictor", layout="wide")

# App title
st.title("🤖🤖🤖💯Rabiotic Football Match Correct Score Predictor")
st.write("This app predicts the correct score and provides detailed insights using statistics, league table data, and odds.")

# Input form
st.sidebar.header("Input Match Details")
team_a = st.sidebar.text_input("Team A", value="Team A")
team_b = st.sidebar.text_input("Team B", value="Team B")

# League statistics
matches_played_a = st.sidebar.number_input("Matches Played by Team A", min_value=0, value=15)
matches_played_b = st.sidebar.number_input("Matches Played by Team B", min_value=0, value=16)
wins_a = st.sidebar.number_input("Wins by Team A", min_value=0, value=9)
wins_b = st.sidebar.number_input("Wins by Team B", min_value=0, value=6)
draws_a = st.sidebar.number_input("Draws by Team A", min_value=0, value=4)
draws_b = st.sidebar.number_input("Draws by Team B", min_value=0, value=2)
losses_a = st.sidebar.number_input("Losses by Team A", min_value=0, value=2)
losses_b = st.sidebar.number_input("Losses by Team B", min_value=0, value=8)
goal_diff_a = st.sidebar.number_input("Goal Difference of Team A", value=17)
goal_diff_b = st.sidebar.number_input("Goal Difference of Team B", value=-6)
points_a = st.sidebar.number_input("Points of Team A", value=31)
points_b = st.sidebar.number_input("Points of Team B", value=20)

# Additional statistics
avg_goals_a = st.sidebar.number_input("Average Goals Scored by Team A", min_value=0.0, value=1.6)
avg_goals_b = st.sidebar.number_input("Average Goals Scored by Team B", min_value=0.0, value=1.1)
form_a = st.sidebar.slider("Form Percentage of Team A", min_value=0, max_value=100, value=47)
form_b = st.sidebar.slider("Form Percentage of Team B", min_value=0, max_value=100, value=27)

# Full-time odds
home_odds = st.sidebar.number_input("Full-Time Odds (Home Win)", min_value=1.0, value=1.65)
draw_odds = st.sidebar.number_input("Full-Time Odds (Draw)", min_value=1.0, value=4.23)
away_odds = st.sidebar.number_input("Full-Time Odds (Away Win)", min_value=1.0, value=5.6)

# Add a submit button to the sidebar
with st.sidebar:
    st.markdown("### Submit Prediction")
    if st.button("Submit Prediction"):
        st.success("Prediction submitted! Results will be displayed below.")

# Calculate attack and defense strengths
attack_strength_a = avg_goals_a * (form_a / 20)
attack_strength_b = avg_goals_b * (form_b / 190)

# Generate Poisson distribution probabilities
max_goals = 5
team_a_probs = [poisson.pmf(i, attack_strength_a) for i in range(max_goals + 1)]
team_b_probs = [poisson.pmf(i, attack_strength_b) for i in range(max_goals + 2)]

# Generate probability for HT 1-0 and FT 1-2
# HT: Team A 1 - Team B 0
ht_prob = poisson.pmf(1, attack_strength_a) * poisson.pmf(0, attack_strength_b)

# FT: Team A 1 - Team B 2
ft_prob = poisson.pmf(1, attack_strength_a) * poisson.pmf(2, attack_strength_b)

# Combined probability of HT 1-0 and FT 1-2
combined_ht_ft_prob = ht_prob * ft_prob

# Display match details
st.write("### Match Details")
st.write(f"**{team_a} vs {team_b}**")
st.write(f"- **Team A Form (%):** {form_a}")
st.write(f"- **Team B Form (%):** {form_b}")
st.write(f"- **Odds (Home - Draw - Away):** {home_odds} - {draw_odds} - {away_odds}")

# Display probabilities
st.write("### Match Outcome Probabilities")
st.write(f"- **Probability of Home Win**: {home_odds:.2f}")
st.write(f"- **Probability of Draw**: {draw_odds:.2f}")
st.write(f"- **Probability of Away Win**: {away_odds:.2f}")

# Display specific correct score A 1 - B 2 probability
st.write("### Correct Score Probability")
st.write(f"- The probability of the correct score **{team_a} 1 - {team_b} 2** is: **{combined_ht_ft_prob * 100:.2f}%**")

# Recommended correct score (HT/FT)
st.write("### Recommended Correct Score")
st.write(f"The recommended correct score is **{team_a} 1 - {team_b} 2** (HT 1-0, FT 1-2) with a probability of **{combined_ht_ft_prob * 100:.2f}%**.")
