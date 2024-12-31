# Importing required libraries
import streamlit as st
import numpy as np
from scipy.stats import poisson

# Title
st.title("💯💯💯🤖🤖🤖🔑🔑🔑⚽⚽⚽ Rabiotic Deep Advanced Football Match ✅Correct score Outcome Analysis Predictor")

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

# Additional Odds for Verification
st.header("Additional Odds for Verification")
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

# Display probabilities for each possible scoreline
scoreline_probs = {}
for i in range(4):  # Goals by Team A
    for j in range(4):  # Goals by Team B
        scoreline_probs[(i, j)] = probs_A[i] * probs_B[j]

# Calculate probabilities for 1x2 outcomes
home_win_prob = sum(prob for (i, j), prob in scoreline_probs.items() if i > j)
draw_prob = sum(prob for (i, j), prob in scoreline_probs.items() if i == j)
away_win_prob = sum(prob for (i, j), prob in scoreline_probs.items() if i < j)

# Normalize probabilities to percentages
total_prob = home_win_prob + draw_prob + away_win_prob
home_win_percent = (home_win_prob / total_prob) * 100
draw_percent = (draw_prob / total_prob) * 100
away_win_percent = (away_win_prob / total_prob) * 100

# Display 1x2 probabilities
st.subheader("1x2 Probability-Based Percentages")
st.write(f"Probability of Home Win: **{home_win_percent:.2f}%**")
st.write(f"Probability of Draw: **{draw_percent:.2f}%**")
st.write(f"Probability of Away Win: **{away_win_percent:.2f}%**")

# Display deep analysis of team goals probabilities
st.subheader("Deep Analysis of Team Goals Probability (%)")
st.write("### Team A (Home)")
for i, prob in enumerate(probs_A):
    st.write(f"Probability of Team A scoring {i if i < 3 else '3+'} goals: **{prob * 100:.2f}%**")

st.write("### Team B (Away)")
for i, prob in enumerate(probs_B):
    st.write(f"Probability of Team B scoring {i if i < 3 else '3+'} goals: **{prob * 100:.2f}%**")

# Calculate Over/Under probabilities
ou_probs = {
    "Over 1.5": 1 - (probs_A[0] * probs_B[0] + probs_A[0] * probs_B[1] + probs_A[1] * probs_B[0]),
    "Under 1.5": probs_A[0] * probs_B[0] + probs_A[0] * probs_B[1] + probs_A[1] * probs_B[0],
    "Over 2.5": 1 - (probs_A[0] * probs_B[0] + probs_A[0] * probs_B[1] + probs_A[1] * probs_B[0] + probs_A[1] * probs_B[1]),
    "Under 2.5": probs_A[0] * probs_B[0] + probs_A[0] * probs_B[1] + probs_A[1] * probs_B[0] + probs_A[1] * probs_B[1],
}

# Calculate GG/NG probabilities
gg_prob = np.sum([probs_A[i] * probs_B[j] for i in range(1, len(probs_A)) for j in range(1, len(probs_B))])
ng_prob = 1 - gg_prob

# Scoreline calculation
scoreline_probs = {}
for i in range(4):  # Possible goals for Team A
    for j in range(4):  # Possible goals for Team B
        scoreline_probs[f"{i}-{j}"] = probs_A[i] * probs_B[j]

# Sort scorelines by probability
sorted_scorelines = sorted(scoreline_probs.items(), key=lambda x: x[1], reverse=True)

# Display top 12 most likely scorelines
st.subheader("Top 12 Most Likely Scorelines")
for i, (scoreline, prob) in enumerate(sorted_scorelines[:12]):
    st.write(f"{scoreline}: **{prob * 100:.2f}%**")

# Top 5 most likely scorelines for recommendation
top_5_scorelines = sorted_scorelines[:5]

# Recommendation based on top scorelines
st.subheader("Recommended Scoreline Bet")
for scoreline, prob in top_5_scorelines:
    st.write(f"Recommended Bet on Scoreline **{scoreline}** with probability **{prob * 100:.2f}%**")

# Probabilities for most likely scorelines (adjustable to real calculations)
scoreline_probs = {
    "0-0": 0.062, "1-0": 0.058, "0-1": 0.057, "1-1": 0.061,
    "2-0": 0.052, "0-2": 0.053, "2-1": 0.059, "1-2": 0.056,
}

# HT/FT probabilities (initially zero, calculated below)
ht_ft_probs = {
    "1/1": 0.0, "1/X": 0.0, "1/2": 0.0,
    "X/1": 0.0, "X/X": 0.0, "X/2": 0.0,
    "2/1": 0.0, "2/X": 0.0, "2/2": 0.0,
}

# HT/FT odds input
st.title("HT/FT & Correct Score Value Bet Calculator")
st.subheader("Input Odds for HT/FT Outcomes")
odds_for_ht_ft = {}
for outcome in ht_ft_probs.keys():
    odds_for_ht_ft[outcome] = st.number_input(
        f"Odds for {outcome}:", min_value=1.0, value=10.0, step=0.1
    )

# Function to calculate HT/FT probabilities based on scorelines
def calculate_ht_ft_probs(scoreline_probs):
    ht_ft_probs = {
        "1/1": 0.0, "1/X": 0.0, "1/2": 0.0,
        "X/1": 0.0, "X/X": 0.0, "X/2": 0.0,
        "2/1": 0.0, "2/X": 0.0, "2/2": 0.0,
    }
    for scoreline, prob in scoreline_probs.items():
        ht, ft = map(int, scoreline.split("-"))

        if ht > ft:  # HT Win
            if ft > ht:  # FT Lose
                ht_ft_probs["1/2"] += prob
            elif ft == ht:  # FT Draw
                ht_ft_probs["1/X"] += prob
            else:  # FT Win
                ht_ft_probs["1/1"] += prob
        elif ht == ft:  # HT Draw
            if ft > ht:  # FT Win
                ht_ft_probs["X/1"] += prob
            elif ft == ht:  # FT Draw
                ht_ft_probs["X/X"] += prob
            else:  # FT Lose
                ht_ft_probs["X/2"] += prob
        else:  # HT Lose
            if ft > ht:  # FT Win
                ht_ft_probs["2/1"] += prob
            elif ft == ht:  # FT Draw
                ht_ft_probs["2/X"] += prob
            else:  # FT Lose
                ht_ft_probs["2/2"] += prob

    return ht_ft_probs

# Calculate HT/FT probabilities
ht_ft_probs = calculate_ht_ft_probs(scoreline_probs)

# Display HT/FT probabilities
st.subheader("HT/FT Probabilities")
for scenario, prob in ht_ft_probs.items():
    st.write(f"{scenario}: **{prob * 100:.2f}%**")

# Find the best HT/FT value bet
def find_best_ht_ft_value_bet(ht_ft_probs, odds_for_ht_ft):
    value_bets = {
        outcome: prob for outcome, prob in ht_ft_probs.items()
        if outcome in odds_for_ht_ft and prob * odds_for_ht_ft[outcome] > 1
    }
    if value_bets:
        best_outcome = max(value_bets, key=value_bets.get)
        return best_outcome, value_bets[best_outcome]
    return None, None

# Best HT/FT value bet
best_ht_ft_outcome, best_ht_ft_prob = find_best_ht_ft_value_bet(ht_ft_probs, odds_for_ht_ft)

# Display the best HT/FT value bet
if best_ht_ft_outcome:
    st.subheader("Best HT/FT Value Bet")
    st.write(f"The best HT/FT value bet is: **{best_ht_ft_outcome}**")
    st.write(f"Probability: **{best_ht_ft_prob * 100:.2f}%**")
    st.write(f"Odds: **{odds_for_ht_ft[best_ht_ft_outcome]}**")
    st.write(f"Expected Value (EV): **{best_ht_ft_prob * odds_for_ht_ft[best_ht_ft_outcome]:.2f}**")
else:
    st.subheader("Best HT/FT Value Bet")
    st.write("No profitable HT/FT value bets found based on the given odds and probabilities.")

# Function to calculate the best value bet for correct scores
def calculate_best_correct_score(scoreline_probs, threshold=0.052):
    """Filters scorelines with probabilities above the threshold."""
    filtered_scores = {
        scoreline: prob for scoreline, prob in scoreline_probs.items() if prob >= threshold
    }
    if filtered_scores:
        best_scoreline = max(filtered_scores, key=filtered_scores.get)
        return best_scoreline, filtered_scores[best_scoreline]
    return None, None

# Calculate the best correct score
best_scoreline, best_score_prob = calculate_best_correct_score(scoreline_probs, threshold=0.052)

# Display the best correct score
if best_scoreline:
    st.subheader("Best Correct Score")
    st.write(f"The most likely correct score: **{best_scoreline}**")
    st.write(f"Probability: **{best_score_prob * 100:.2f}%**")
else:
    st.subheader("Best Correct Score")
    st.write("No scoreline exceeds the probability threshold.")

# Final recommendation based on the highest value bet
if best_ht_ft_outcome and best_scoreline:
    st.subheader("Final Recommendation")
    st.write(f"Recommended HT/FT Outcome: **{best_ht_ft_outcome}**")
    st.write(f"Recommended Correct Score: **{best_scoreline}**")
else:
    st.subheader("Final Recommendation")
    st.write("Not enough data for a confident recommendation.")

# Value odds calculation
def calculate_value(probability, odds):
    return probability * odds > 1

# Display odds verification
st.subheader("Odds Value Verification")
st.write(f"Over 1.5 Goals: {'Value Bet' if calculate_value(ou_probs['Over 1.5'], odds_over_1_5) else 'No Value'}")
st.write(f"Under 1.5 Goals: {'Value Bet' if calculate_value(ou_probs['Under 1.5'], odds_under_1_5) else 'No Value'}")
st.write(f"Over 2.5 Goals: {'Value Bet' if calculate_value(ou_probs['Over 2.5'], odds_over_2_5) else 'No Value'}")
st.write(f"Under 2.5 Goals: {'Value Bet' if calculate_value(ou_probs['Under 2.5'], odds_under_2_5) else 'No Value'}")
st.write(f"Both Teams to Score (GG): {'Value Bet' if calculate_value(gg_prob, odds_btts_gg) else 'No Value'}")
st.write(f"Both Teams Not to Score (NG): {'Value Bet' if calculate_value(ng_prob, odds_btts_ng) else 'No Value'}")

st.write("### Over/Under Recommendations")
for key, value in ou_probs.items():
    st.write(f"Probability of {key}: **{value * 100:.2f}%**")
st.write(f"Recommendation: Bet on **{'Over' if ou_probs['Over 2.5'] > 0.5 else 'Under'} 2.5 Goals**")

st.write("### GG/NG Recommendations")
st.write(f"Probability of GG: **{gg_prob * 100:.2f}%**")
st.write(f"Probability of NG: **{ng_prob * 100:.2f}%**")
st.write(f"Recommendation: Bet on **{'GG' if gg_prob > 0.5 else 'NG'}**")

# Calculate value bets for correct scores
def calculate_value_bet_correct_score(scoreline_probs, odds_for_scoreline):
    """Finds the highest probability correct score that is also a profitable value bet."""
    value_bets = {
        scoreline: prob for scoreline, prob in scoreline_probs.items()
        if scoreline in odds_for_scoreline and prob * odds_for_scoreline[scoreline] > 1
    }
    if value_bets:
        best_value_scoreline = max(value_bets, key=value_bets.get)
        return best_value_scoreline, value_bets[best_value_scoreline]
    else:
        return None, None

# Example probabilities for correct scores (Replace with actual calculations)
scoreline_probs = {
    "0-0": 0.08, "1-0": 0.12, "0-1": 0.10, "1-1": 0.15,
    "2-0": 0.06, "0-2": 0.05, "2-1": 0.09, "1-2": 0.07,
    "3-0": 0.03, "0-3": 0.02, "3-1": 0.04, "1-3": 0.03,
    "2-2": 0.08, "3-2": 0.02, "2-3": 0.01, "4-0": 0.01,
    "0-4": 0.01, "4-1": 0.01, "1-4": 0.01, "4-2": 0.01,
    "2-4": 0.01, "4-3": 0.01, "3-4": 0.01, "4-4": 0.005,
}

# Initial probabilities for scorelines (replace with actual calculations or inputs)
scoreline_probs = {
    "0-0": 0.08, "1-0": 0.12, "0-1": 0.10, "1-1": 0.15,
    "2-0": 0.06, "0-2": 0.05, "2-1": 0.09, "1-2": 0.07,
    "3-0": 0.03, "0-3": 0.02, "3-1": 0.04, "1-3": 0.03,
    "2-2": 0.08, "3-2": 0.02, "2-3": 0.01, "4-0": 0.01,
    "0-4": 0.01, "4-1": 0.01, "1-4": 0.01, "4-2": 0.01,
    "2-4": 0.01, "4-3": 0.01, "3-4": 0.01, "4-4": 0.005,
}


# HT/FT probabilities (adjust as needed)
ht_ft_probabilities = {
    "1/1": 40.0, "1/X": 10.0, "1/2": 5.0,
    "X/1": 20.0, "X/X": 15.0, "X/2": 5.0,
    "2/1": 5.0, "2/X": 5.0, "2/2": 10.0
}
# Streamlit app title and description
st.title("Value Bet Correct Score & HT/FT Probabilities")
st.write("Input the odds for correct scorelines from 0-0 to 4-4 to calculate the best value bet.")

# Input section for odds
odds_for_scoreline = {}
for scoreline in scoreline_probs.keys():
    odds_for_scoreline[scoreline] = st.number_input(
        f"Odds for {scoreline}:", min_value=1.0, value=10.0, step=0.1
    )

# Step 1: Adjust probabilities using a scaling factor
scaling_factor = 6.19 / 5.28  # Example adjustment
adjusted_scorelines = {
    score: round(prob * scaling_factor, 2) for score, prob in scoreline_probs.items()
}

# Step 2: Normalize adjusted probabilities to sum to 100%
total_prob = sum(adjusted_scorelines.values())
adjusted_scorelines = {
    score: round(prob / total_prob * 100, 2) for score, prob in adjusted_scorelines.items()
}

# Step 3: Combine HT/FT probabilities with adjusted scoreline probabilities
combined_probabilities = {}
for score, score_prob in adjusted_scorelines.items():
    ht_key = "1/1" if score in ["1:0", "2:0", "3:1"] else "X/X"  # Example mapping
    ht_prob = ht_ft_probabilities.get(ht_key, 0)
    combined_probabilities[score] = round(score_prob * (ht_prob / 100), 2)

# Step 4: Calculate value bets for correct scores
def calculate_value_bet_correct_score(scoreline_probs, odds_for_scoreline):
    value_bets = {
        scoreline: prob for scoreline, prob in scoreline_probs.items()
        if scoreline in odds_for_scoreline and prob * odds_for_scoreline[scoreline] > 1
    }
    if value_bets:
        best_value_scoreline = max(value_bets, key=value_bets.get)
        return best_value_scoreline, value_bets[best_value_scoreline]
    return None, None

# Find the best value bet correct score
best_value_scoreline, best_value_prob = calculate_value_bet_correct_score(
    adjusted_scorelines, odds_for_scoreline
)

# Step 5: Display results
st.subheader("Adjusted Scoreline Probabilities")
st.write(adjusted_scorelines)

st.subheader("Combined Probabilities")
st.write(combined_probabilities)

st.subheader("Top 7 Value Bet Correct Scorelines")

# Ensure best_scorelines is a list of tuples with scoreline, probability, and odds
if scoreline_probabilities and odds_for_scoreline:
    # Calculate EV for all scorelines
    scoreline_ev = [
        (scoreline, prob, odds_for_scoreline[scoreline], prob * odds_for_scoreline[scoreline])
        for scoreline, prob in scoreline_probabilities.items()
        if scoreline in odds_for_scoreline  # Ensure the scoreline has odds
    ]

    # Sort by Expected Value (EV) in descending order
    scoreline_ev = sorted(scoreline_ev, key=lambda x: x[3], reverse=True)

    # Select the top 7 scorelines
    top_7_scorelines = scoreline_ev[:7]

    # Display the results
    for i, (scoreline, prob, odds, ev) in enumerate(top_7_scorelines, start=1):
        st.write(f"**#{i} Scoreline:** {scoreline}")
        st.write(f"   - **Probability:** {prob * 100:.2f}%")
        st.write(f"   - **Odds:** {odds}")
        st.write(f"   - **Expected Value (EV):** {ev:.2f}")
        st.write("---")  # Add a separator between scorelines

else:
    st.write("No data available for scorelines or odds.")


# Find the Top 7 most likely scorelines best value bet correct score
best_value_scoreline, best_value_prob = calculate_value_bet_correct_score(scoreline_probs, odds_for_scoreline)

# Display the best value bet correct score
if best_value_scoreline:
    st.subheader("Value Bet Correct Score")
    st.write(f"The correct score with the highest probability that is also a value bet: **{best_value_scoreline}**")
    st.write(f"Probability: **{best_value_prob * 100:.2f}%**")
    st.write(f"Odds: **{odds_for_scoreline[best_value_scoreline]}**")
    st.write(f"Expected Value (EV): **{best_value_prob * odds_for_scoreline[best_value_scoreline]:.2f}**")
else:
    st.subheader("Value Bet Correct Score")
    st.write("No profitable value bet for correct scores based on the given odds.")

# Determine final correct score based on combined recommendations
st.subheader("Combined Recommendations (Over/Under 2.5 & GG/NG)")
if ou_probs["Over 2.5"] > 0.5 and gg_prob > 0.5:
    combined_recommendation = "Over 2.5 & GG"
    final_correct_score = next((scoreline for scoreline, prob in sorted_scorelines if int(scoreline.split("-")[0]) > 1 and int(scoreline.split("-")[1]) > 0), "2-1")
elif ou_probs["Under 2.5"] > 0.5 and ng_prob > 0.5:
    combined_recommendation = "Under 2.5 & NG"
    final_correct_score = next((scoreline for scoreline, prob in sorted_scorelines if int(scoreline.split("-")[0]) + int(scoreline.split("-")[1]) <= 2 and (int(scoreline.split("-")[0]) == 0 or int(scoreline.split("-")[1]) == 0)), "1-0")
else:
    combined_recommendation = "No Clear Combined Option"
    final_correct_score = sorted_scorelines[0][0]

st.write(f"Recommendation: Bet on **{combined_recommendation}**")
st.write(f"Final 1x2 Probability-Based Percentages Correct Score Prediction: **{final_correct_score}**")
# Step 1: Define the original probabilities for the top 12 scorelines
scoreline_probabilities = [
    {"scoreline": "1:0", "probability": 5.28},
    {"scoreline": "1:1", "probability": 6.19},
    {"scoreline": "2:1", "probability": 4.75},
    {"scoreline": "0:0", "probability": 3.84},
    {"scoreline": "2:0", "probability": 3.65},
    {"scoreline": "0:1", "probability": 3.21},
    {"scoreline": "1:2", "probability": 3.15},
    {"scoreline": "3:1", "probability": 2.89},
    {"scoreline": "1:3", "probability": 2.45},
    {"scoreline": "2:2", "probability": 2.31},
    {"scoreline": "0:2", "probability": 2.14},
    {"scoreline": "3:0", "probability": 1.97},
]

# Step 2: Normalize probabilities to ensure they sum to 100%
total_prob = sum(item["probability"] for item in scoreline_probabilities)
for item in scoreline_probabilities:
    item["normalized_probability"] = (item["probability"] / total_prob) * 100

# Step 3: Apply matrix weighting adjustment
# Define the adjustment factor (e.g., +10%)
adjustment_factor = 1.10  # This increases probabilities by 10%

adjusted_probabilities = []
for item in scoreline_probabilities:
    adjusted_probability = item["normalized_probability"] * adjustment_factor
    adjusted_probabilities.append({
        "scoreline": item["scoreline"],
        "adjusted_probability": adjusted_probability
    })

# Step 4: Find the matrix-recommended correct score
matrix_recommendation = max(adjusted_probabilities, key=lambda x: x["adjusted_probability"])

# Define the Final 1x2 Prediction (example values)
final_1x2_prediction = {
    "1": 45,  # Home win percentage
    "X": 30,  # Draw percentage
    "2": 25   # Away win percentage
}

# Step 5: Output the results
final_output = {
    "Final 1x2 Prediction": final_1x2_prediction,
    "Matrix Recommendation": {
        "Correct Score": matrix_recommendation["scoreline"],
        "Probability": round(matrix_recommendation["adjusted_probability"], 2)
    }
}

# Display the results
print("Final 1x2 Prediction:")
for result, percentage in final_output["Final 1x2 Prediction"].items():
    print(f"  {result}: {percentage}%")

print("\nMatrix Recommendation:")
print(f"  Correct Score: {final_output['Matrix Recommendation']['Correct Score']}")
print(f"  Probability: {final_output['Matrix Recommendation']['Probability']}%")
