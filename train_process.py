import pandas as pd
from sklearn.svm import OneClassSVM
import joblib

print("1. Loading ONLY the Clean BATADAL Dataset...")
# Use ONLY the file that you know has zero anomalies in it!
df = pd.read_csv('BATADAL_Train_1.csv') 

print("2. Cleaning Data (Dropping Time & Flags)...")
columns_to_drop = ['DATETIME', 'ATT_FLAG', 'label']
for col in columns_to_drop:
    if col in df.columns:
        df = df.drop(col, axis=1)

numeric_df = df.select_dtypes(include=['float64', 'int64']).fillna(0)

print("3. Training the One-Class SVM (Building the Clean Fence)...")
# nu=0.01 is perfect for clean data.
model = OneClassSVM(nu=0.01, kernel="rbf", gamma="scale")
model.fit(numeric_df)
print("Model trained successfully on pure data!")

print("4. Saving the Process AI Brain...")
joblib.dump(model, 'process_brain.pkl')
print("Saved as 'process_brain.pkl'. The contaminated brain has been overwritten!")