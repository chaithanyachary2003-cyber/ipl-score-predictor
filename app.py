import streamlit as st
import pandas as pd
import pickle

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="IPL Score Predictor",
    page_icon="🏏",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

h1, h2, h3, h4 {
    color: white;
}

.stButton>button {
    width: 100%;
    height: 3em;
    border-radius: 10px;
    font-size: 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================
# Load Model
# =========================

model = pickle.load(
    open('ipl_score_predictor.pkl', 'rb')
)

# =========================
# App Title
# =========================

st.markdown("""
# 🏏 IPL Final Score Predictor

### AI Powered Cricket Analytics System
""")

# =========================
# SIDEBAR
# =========================

st.sidebar.title("Dashboard")

st.sidebar.markdown("""
## About Project

This system predicts:

- IPL Final Score
- Match Momentum
- Run Rate Analysis

### Technologies Used

- Python
- Pandas
- XGBoost
- Streamlit
""")

st.markdown("---")

# =========================
# Teams
# =========================

teams = [
    'Chennai Super Kings',
    'Deccan Chargers',
    'Delhi Capitals',
    'Delhi Daredevils',
    'Gujarat Lions',
    'Gujarat Titans',
    'Kings XI Punjab',
    'Kochi Tuskers Kerala',
    'Kolkata Knight Riders',
    'Lucknow Super Giants',
    'Mumbai Indians',
    'Pune Warriors',
    'Punjab Kings',
    'Rajasthan Royals',
    'Rising Pune Supergiant',
    'Rising Pune Supergiants',
    'Royal Challengers Bangalore',
    'Royal Challengers Bengaluru',
    'Sunrisers Hyderabad'
]

# =========================
# User Inputs
# =========================

col1, col2 = st.columns(2)

with col1:

    batting_team = st.selectbox(
        "Select Batting Team",
        teams
    )

with col2:

    bowling_team = st.selectbox(
        "Select Bowling Team",
        teams
    )


st.subheader("Current Match Situation")

col3, col4, col5 = st.columns(3)


with col3:

    runs = st.number_input(
        "Current Score",
        min_value=0,
        max_value=300,
        step=1
    )

with col4:

    wickets = st.number_input(
        "Wickets Lost",
        min_value=0,
        max_value=10,
        step=1
    )

with col5:

    overs = st.number_input(
        "Overs Completed",
        min_value=0.0,
        max_value=20.0,
        step=0.1
    )

if batting_team == bowling_team:

    st.error(
        "Batting Team and Bowling Team cannot be same"
    )

    st.stop()


# =========================
# Prediction
# =========================

if st.button("Predict Final Score"):

    # Current Run Rate
    if overs == 0:
        crr = 0
    else:
        crr = runs / overs

    # Balls Left
    balls_left = 120 - int(overs * 6)

    # Base Features
    input_data = {
        'innings': 1,
        'over': int(overs),
        'ball': 0,
        'team_runs': runs,
        'team_wicket': wickets,
        'current_over': overs,
        'balls_left': balls_left,
        'crr': crr
    }

    # ALL TRAINING COLUMNS
    all_columns = [
        'batting_team_Chennai Super Kings',
        'batting_team_Deccan Chargers',
        'batting_team_Delhi Capitals',
        'batting_team_Delhi Daredevils',
        'batting_team_Gujarat Lions',
        'batting_team_Gujarat Titans',
        'batting_team_Kings XI Punjab',
        'batting_team_Kochi Tuskers Kerala',
        'batting_team_Kolkata Knight Riders',
        'batting_team_Lucknow Super Giants',
        'batting_team_Mumbai Indians',
        'batting_team_Pune Warriors',
        'batting_team_Punjab Kings',
        'batting_team_Rajasthan Royals',
        'batting_team_Rising Pune Supergiant',
        'batting_team_Rising Pune Supergiants',
        'batting_team_Royal Challengers Bangalore',
        'batting_team_Royal Challengers Bengaluru',
        'batting_team_Sunrisers Hyderabad',

        'bowling_team_Chennai Super Kings',
        'bowling_team_Deccan Chargers',
        'bowling_team_Delhi Capitals',
        'bowling_team_Delhi Daredevils',
        'bowling_team_Gujarat Lions',
        'bowling_team_Gujarat Titans',
        'bowling_team_Kings XI Punjab',
        'bowling_team_Kochi Tuskers Kerala',
        'bowling_team_Kolkata Knight Riders',
        'bowling_team_Lucknow Super Giants',
        'bowling_team_Mumbai Indians',
        'bowling_team_Pune Warriors',
        'bowling_team_Punjab Kings',
        'bowling_team_Rajasthan Royals',
        'bowling_team_Rising Pune Supergiant',
        'bowling_team_Rising Pune Supergiants',
        'bowling_team_Royal Challengers Bangalore',
        'bowling_team_Royal Challengers Bengaluru',
        'bowling_team_Sunrisers Hyderabad'
    ]

    # Initialize all columns with 0
    for col in all_columns:
        input_data[col] = 0

    # Set selected batting team
    batting_col = f'batting_team_{batting_team}'
    if batting_col in input_data:
        input_data[batting_col] = 1

    # Set selected bowling team
    bowling_col = f'bowling_team_{bowling_team}'
    if bowling_col in input_data:
        input_data[bowling_col] = 1

    # Create DataFrame
    input_df = pd.DataFrame([input_data])

    with st.spinner("Analyzing Match Situation..."):

        prediction = model.predict(input_df)

predicted_score = int(prediction[0])

st.success(
    f"Predicted Final Score: {predicted_score}"
)

col6, col7, col8 = st.columns(3)

with col6:
    st.metric(
        "Current Run Rate",
        round(crr, 2)
    )

with col7:
    st.metric(
        "Predicted Score",
        predicted_score
    )

with col8:
    st.metric(
        "Projected Range",
        f"{predicted_score-10} - {predicted_score+10}"
    )

# =========================
# MATCH PROGRESS
# =========================

st.subheader("Match Progress")

progress = int((overs / 20) * 100)

st.progress(progress)

st.write(
    f"{progress}% Innings Completed"
)

# =========================
# MATCH SUMMARY
# =========================

st.subheader("Match Summary")

st.write(f"""
### {batting_team} vs {bowling_team}

- Current Score: {runs}/{wickets}
- Overs Completed: {overs}
- Current Run Rate: {round(crr,2)}
- Predicted Final Score: {predicted_score}
""")

st.markdown("---")

st.caption(
    "Developed using Machine Learning, XGBoost and Streamlit"
)
