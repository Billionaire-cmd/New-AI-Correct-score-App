import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import poisson
import requests

# Title and Sidebar
st.title("HT/FT Correct Score Prediction App")
st.sidebar.header("Match Settings")
st.sidebar.write("Adjust parameters for predictions.")

# Load Data
@st.cache_data
def load_data():
    # Example placeholder data; replace with real historical match data
    data = pd.read_csv("historical_data.csv")  # Replace with actual dataset
    return data

data = load_data()

# Preprocessing
@st.cache_data
def preprocess_data(data):
    # Create features like goal difference, recent form, etc.
    data['goal_diff'] = data['home_goals'] - data['away_goals']
    data['recent_form'] = data['home_points'] * 0.6 + data['away_points'] * 0.4
    data['head_to_head'] = data.groupby(['team_home', 'team_away'])['result'].transform('mean')
    return data

processed_data = preprocess_data(data)

# User Input
team_list = processed_data['team_home'].unique()
selected_team_a = st.sidebar.selectbox("Select Team A", team_list)
selected_team_b = st.sidebar.selectbox("Select Team B", team_list)

# Filter Data for Selected Teams
match_data = processed_data[
    (processed_data['team_home'] == selected_team_a) &
    (processed_data['team_away'] == selected_team_b)
]

# Train/Test Split
X = processed_data[['home_goals', 'away_goals', 'goal_diff', 'recent_form', 'head_to_head']]
y_ht = processed_data['ht_score']  # Halftime correct scores
y_ft = processed_data['ft_score']  # Full-time correct scores

X_train, X_test, y_ht_train, y_ht_test = train_test_split(X, y_ht, test_size=0.2, random_state=42)
X_train, X_test, y_ft_train, y_ft_test = train_test_split(X, y_ft, test_size=0.2, random_state=42)

# Train Models
@st.cache_resource
def train_models():
    ht_model = RandomForestClassifier(random_state=42)
    ft_model = RandomForestClassifier(random_state=42)
    ht_model.fit(X_train, y_ht_train)
    ft_model.fit(X_train, y_ft_train)
    return ht_model, ft_model

ht_model, ft_model = train_models()

# Predictions
def predict_scores(model, X):
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)
    return predictions, probabilities

ht_predictions, ht_probs = predict_scores(ht_model, X_test)
ft_predictions, ft_probs = predict_scores(ft_model, X_test)

# Accuracy
ht_accuracy = accuracy_score(y_ht_test, ht_predictions)
ft_accuracy = accuracy_score(y_ft_test, ft_predictions)

st.sidebar.write(f"HT Model Accuracy: {ht_accuracy:.2%}")
st.sidebar.write(f"FT Model Accuracy: {ft_accuracy:.2%}")

# Score Probability Heatmap
def plot_heatmap(prob_matrix, title):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(prob_matrix, annot=True, fmt=".2%", cmap="YlGnBu", cbar=True, ax=ax)
    ax.set_title(title)
    return fig

ht_prob_matrix = pd.DataFrame(ht_probs, columns=ht_model.classes_)
ft_prob_matrix = pd.DataFrame(ft_probs, columns=ft_model.classes_)

st.subheader("Halftime Score Probabilities")
st.pyplot(plot_heatmap(ht_prob_matrix.values, "Halftime Probabilities"))

st.subheader("Full-time Score Probabilities")
st.pyplot(plot_heatmap(ft_prob_matrix.values, "Full-time Probabilities"))

# Match Simulation
def simulate_match(home_avg, away_avg, simulations=1000):
    results = {"Home Wins": 0, "Draws": 0, "Away Wins": 0}
    for _ in range(simulations):
        home_goals = np.random.poisson(home_avg)
        away_goals = np.random.poisson(away_avg)
        if home_goals > away_goals:
            results["Home Wins"] += 1
        elif home_goals == away_goals:
            results["Draws"] += 1
        else:
            results["Away Wins"] += 1
    return results

sim_results = simulate_match(1.5, 1.2)
st.sidebar.write("Simulation Results:")
st.sidebar.write(sim_results)

# Real-Time Data Integration
def fetch_live_data(team_a, team_b):
    api_key = "YOUR_API_KEY"  # Replace with your API key
    url = f"https://api.football-data.org/v4/matches?teamA={team_a}&teamB={team_b}"
    headers = {"X-Auth-Token": api_key}
    response = requests.get(url, headers=headers).json()
    return response

# Downloadable Predictions
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

prediction_df = pd.DataFrame({
    "Team A": [selected_team_a],
    "Team B": [selected_team_b],
    "Predicted HT Score": ht_predictions,
    "Predicted FT Score": ft_predictions
})

st.download_button(
    label="Download Predictions as CSV",
    data=convert_df_to_csv(prediction_df),
    file_name='predictions.csv',
    mime='text/csv',
)

# Footer
st.write("Powered by advanced machine learning and statistical models!")
