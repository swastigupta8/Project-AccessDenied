import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

print("1. Loading Windows 10 IT/Network Data...")
# We make sure it trains on the exact same file we are testing!
df = pd.read_csv('Train_Test_Windows_10.csv') 

print("2. Cleaning Data (Dropping Text & Labels)...")
if 'label' in df.columns:
    df = df.drop('label', axis=1)

# Keep only the numbers
numeric_df = df.select_dtypes(include=['float64', 'int64']).fillna(0)

print("3. Retraining the Isolation Forest...")
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(numeric_df)
print("Model trained successfully!")

print("4. Saving the New AI Brain...")
joblib.dump(model, 'network_brain.pkl')
print("Saved! The brain and the test script are now perfectly synced.")