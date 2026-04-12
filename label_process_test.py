import joblib
import pandas as pd

# 1. Load the model and the test data
model = joblib.load('process_brain.pkl')
df = pd.read_csv('BATADAL_Train_2.csv') # Or your specific test file name

# 2. Prep the data (dropping non-numeric columns)
# We keep a copy of the original to save the labels back into it
original_df = df.copy()
columns_to_drop = ['DATETIME', 'ATT_FLAG', 'label']
for col in columns_to_drop:
    if col in df.columns:
        df = df.drop(col, axis=1)

numeric_df = df.select_dtypes(include=['float64', 'int64']).fillna(0)

# 3. Run the AI on the whole file
print("Analyzing Process Data...")
raw_scores = model.decision_function(numeric_df)

# 4. Apply your Confidence Logic to create the labels
def get_label(score):
    if score < -5.0: return "HIGH"
    elif score < 0.0: return "MEDIUM"
    else: return "LOW"

original_df['AI_THREAT_SCORE'] = raw_scores
original_df['AI_THREAT_LEVEL'] = [get_label(s) for s in raw_scores]

# 5. Save the labeled file
original_df.to_csv('LABELED_Process_Test.csv', index=False)
print("Done! Check 'LABELED_Process_Test.csv'")
print("Average AI Score:", sum(raw_scores) / len(raw_scores))