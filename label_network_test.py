import joblib
import pandas as pd

# 1. Load the model and the test data
model = joblib.load('network_brain.pkl')
df = pd.read_csv('Train_Test_Windows_10.csv')

# 2. Prep the data using the AI's memorized features
expected_columns = model.feature_names_in_
original_df = df.copy()

# Ensure the test file has the columns the AI expects
for col in expected_columns:
    if col not in df.columns:
        df[col] = 0

numeric_df = df[expected_columns].fillna(0)

# 3. Run the AI
print("Analyzing Network Data...")
raw_scores = model.decision_function(numeric_df)

# 4. Apply Network Confidence Logic (Isolation Forest math)
def get_label(score):
    if score < -0.15: return "HIGH"
    elif score < 0.0: return "MEDIUM"
    else: return "LOW"

original_df['AI_THREAT_SCORE'] = raw_scores
original_df['AI_THREAT_LEVEL'] = [get_label(s) for s in raw_scores]

# 5. Save the labeled file
original_df.to_csv('LABELED_Network_Test.csv', index=False)
print("Done! Check 'LABELED_Network_Test.csv'")