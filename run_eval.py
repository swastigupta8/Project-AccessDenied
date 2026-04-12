import pandas as pd
import joblib
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

print("🚀 Starting Advanced Process Data Evaluation...")

# 1. Load the files
df_train = pd.read_csv('BATADAL_Train_1.csv')
df_test = pd.read_csv('BATADAL_Train_2.csv')

# Clean hidden spaces
df_train.columns = df_train.columns.str.strip()
df_test.columns = df_test.columns.str.strip()
features = [c for c in df_train.columns if c not in ['DATETIME', 'ATT_FLAG', 'label']]

X_train = df_train[features].fillna(0)
X_test = df_test[features].fillna(0)

# 2. THE FIX 1: Scale the Data
print("⚖️ Applying Standard Scaler...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 3. Train the calibrated SVM
print("🧠 Training Support Vector Machine...")
model = OneClassSVM(nu=0.1, kernel="rbf", gamma="scale")
model.fit(X_train_scaled)

# 4. Analyze Test Dataset
print("🔍 Analyzing Test Dataset...")
raw_scores = model.decision_function(X_test_scaled)

# 5. THE FIX 2: Time-Series Smoothing (7-Hour Rolling Average)
print("🌊 Applying Time-Series Smoothing...")
smoothed_scores = pd.Series(raw_scores).rolling(window=7, min_periods=1).mean()

# 6. Apply tuned thresholds
def get_label(score):
    if score < -39.0: return "HIGH"
    elif score < -20.0: return "MEDIUM"
    else: return "LOW"

df_test['AI_THREAT_SCORE'] = smoothed_scores
df_test['AI_THREAT_LEVEL'] = [get_label(s) for s in smoothed_scores]

# 7. Calculate Judge Metrics
truth = [1 if x == 1 else 0 for x in df_test['ATT_FLAG']]
# AI Guess: HIGH or MEDIUM means Attack (1)
predictions = [1 if s < -20.0 else 0 for s in smoothed_scores]

print("\n📊 === AI PERFORMANCE METRICS ===")
print(f"Accuracy:  {accuracy_score(truth, predictions) * 100:.2f}%")
print(f"Precision: {precision_score(truth, predictions, zero_division=0) * 100:.2f}%")
print(f"Recall:    {recall_score(truth, predictions, zero_division=0) * 100:.2f}%")
print(f"F1 Score:  {f1_score(truth, predictions, zero_division=0) * 100:.2f}%")
print("=================================\n")

# Save for the React Frontend
output_file = 'LABELED_Process_Test.csv'
df_test.to_csv(output_file, index=False)
print(f"✅ Success! Saved to {output_file}")