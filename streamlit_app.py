import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson

# Set page configuration
st.set_page_config(page_title="HT/FT Score Predictor", layout="wide")

# Title
st.title("Halftime and Full-time Score Predictor")

# Sidebar inputs
st.sidebar.header("Match Data Input")
team_a = st.sidebar.text_input("Team A", "Team A")
team_b = st.sidebar.text_input("Team B", "Team B")
avg_goals_a = st.sidebar.number_input("Average Goals by Team A", min_value=0.0, value=1.2)
avg_goals_b = st.sidebar.number_input("Average Goals by Team B", min_value=0.0, value=1.1)
odds_a_win = st.sidebar.number_input("Odds for Team A Win", min_value=1.0, value=2.5)
odds_b_win = st.sidebar.number_input("Odds for Team B Win", min_value=1.0, value=2.8)
odds_draw = st.sidebar.number_input("Odds for Draw", min_value=1.0, value=3.0)

# Prediction logic
st.subheader(f"Prediction for {team_a} vs {team_b}")

# Poisson distribution for halftime and full-time scores
def poisson_prob(mean, score):
    return poisson.pmf(score, mean)

# Generate probabilities for scorelines
max_goals = 5
ht_prob_matrix = np.zeros((max_goals+1, max_goals+1))
ft_prob_matrix = np.zeros((max_goals+1, max_goals+1))

for i in range(max_goals+1):
    for j in range(max_goals+1):
        ht_prob_matrix[i, j] = poisson_prob(avg_goals_a / 2, i) * poisson_prob(avg_goals_b / 2, j)
        ft_prob_matrix[i, j] = poisson_prob(avg_goals_a, i) * poisson_prob(avg_goals_b, j)

# Convert to DataFrame for display
ht_df = pd.DataFrame(ht_prob_matrix, columns=[f"{team_b} {j}" for j in range(max_goals+1)], 
                     index=[f"{team_a} {i}" for i in range(max_goals+1)])
ft_df = pd.DataFrame(ft_prob_matrix, columns=[f"{team_b} {j}" for j in range(max_goals+1)], 
                     index=[f"{team_a} {i}" for i in range(max_goals+1)])

# Display probabilities
st.write("### Halftime Correct Score Probabilities")
st.dataframe(ht_df.style.background_gradient(cmap="Blues"))

st.write("### Full-time Correct Score Probabilities")
st.dataframe(ft_df.style.background_gradient(cmap="Greens"))

# Most likely scores
ht_most_likely = np.unravel_index(np.argmax(ht_prob_matrix), ht_prob_matrix.shape)
ft_most_likely = np.unravel_index(np.argmax(ft_prob_matrix), ft_prob_matrix.shape)

st.write(f"Most likely **halftime score**: {team_a} {ht_most_likely[0]} - {team_b} {ht_most_likely[1]}")
st.write(f"Most likely **full-time score**: {team_a} {ft_most_likely[0]} - {team_b} {ft_most_likely[1]}")

# Add interactivity for additional metrics if needed
if st.sidebar.checkbox("Show advanced metrics"):
    st.write("### Advanced Metrics Coming Soon!")

# Footer
st.markdown("### Powered by Poisson Distribution and Machine Learning")
