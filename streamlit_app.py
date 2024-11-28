import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from scipy.stats import poisson

# --- Helper Functions ---
def poisson_probability(avg_goals, actual_goals):
    return poisson.pmf(actual_goals, avg_goals)

def calculate_goal_probabilities(avg_home, avg_away):
    max_goals = 5  # Predict scores up to 5 goals
    probabilities = np.zeros((max_goals+1, max_goals+1))
    for i in range(max_goals+1):
        for j in range(max_goals+1):
            probabilities[i, j] = poisson_probability(avg_home, i) * poisson_probability(avg_away, j)
    return probabilities

# --- Streamlit App ---
st.title("⚽🤖Football Match Predictor: HT/FT Correct Scores")

# Upload historical data
st.sidebar.header("Upload Historical Match Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    # Load data
    data = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Preview")
    st.dataframe(data.head())

    # Train the model
    st.sidebar.header("Train Model")
    if st.sidebar.button("Train Model"):
        # Prepare data
        features = data[['avg_home_goals', 'avg_away_goals', 'home_form', 'away_form']]
        labels_ht = data['ht_score']
        labels_ft = data['ft_score']
        
        X_train, X_test, y_train_ht, y_test_ht = train_test_split(features, labels_ht, test_size=0.2, random_state=42)
        _, _, y_train_ft, y_test_ft = train_test_split(features, labels_ft, test_size=0.2, random_state=42)
        
        # Train HT model
        ht_model = RandomForestClassifier(random_state=42)
        ht_model.fit(X_train, y_train_ht)
        ht_predictions = ht_model.predict(X_test)
        ht_accuracy = accuracy_score(y_test_ht, ht_predictions)
        
        # Train FT model
        ft_model = RandomForestClassifier(random_state=42)
        ft_model.fit(X_train, y_train_ft)
        ft_predictions = ft_model.predict(X_test)
        ft_accuracy = accuracy_score(y_test_ft, ft_predictions)
        
        st.success(f"HT Model Trained with {ht_accuracy*100:.2f}% Accuracy")
        st.success(f"FT Model Trained with {ft_accuracy*100:.2f}% Accuracy")

# Input Team Data for Prediction
st.sidebar.header("Predict HT/FT Scores")
team_a = st.sidebar.text_input("Team A Name", "Team A")
team_b = st.sidebar.text_input("Team B Name", "Team B")
avg_home_goals = st.sidebar.number_input("Team A Avg Goals Scored (Home)", value=1.5)
avg_away_goals = st.sidebar.number_input("Team B Avg Goals Scored (Away)", value=1.2)
home_form = st.sidebar.number_input("Team A Form (last 5 matches)", value=3.0)
away_form = st.sidebar.number_input("Team B Form (last 5 matches)", value=2.5)

if st.sidebar.button("Predict"):
    # Calculate goal probabilities
    goal_probs = calculate_goal_probabilities(avg_home_goals, avg_away_goals)
    
    # Display HT/FT predictions
    st.write(f"### Predictions for {team_a} vs {team_b}")
    st.write("#### Halftime (HT) Score Probabilities:")
    ht_probs = pd.DataFrame(goal_probs, columns=[f"Team B {i}" for i in range(goal_probs.shape[1])], 
                             index=[f"Team A {i}" for i in range(goal_probs.shape[0])])
    st.table(ht_probs)

    st.write("#### Fulltime (FT) Score Probabilities:")
    ft_probs = ht_probs.copy()  # Assuming similar logic for FT (extendable for additional logic)
    st.table(ft_probs)

    st.write("#### Recommended Correct Scores:")
    ht_best = np.unravel_index(np.argmax(goal_probs), goal_probs.shape)
    st.write(f"Halftime: {team_a} {ht_best[0]} - {ht_best[1]} {team_b}")
    st.write(f"Fulltime: {team_a} {ht_best[0]} - {ht_best[1]} {team_b}")
