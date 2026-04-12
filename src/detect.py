import pandas as pd
import numpy as np
import joblib
import os

def detect_anomalies():
    print("Loading the trained AI Brain...")
    model = joblib.load('../models/batadal_ocsvm.pkl')
    scaler = joblib.load('../models/batadal_scaler.pkl')

    print("Loading the 6-month Test Dataset...")
    data_path = '../data/batadal_test.csv'
    df_test = pd.read_csv(data_path)

    # Clean the columns
    df_test.columns = df_test.columns.str.strip().str.upper()

    # Drop non-sensor columns
    columns_to_drop = ['DATETIME', 'ATT_FLAG', 'ATTACK']
    features_test = df_test.drop(columns=[col for col in columns_to_drop if col in df_test.columns])

    print("Scaling test data...")
    scaled_test_features = scaler.transform(features_test)

    print("Analyzing sensor patterns for anomalies...")
    # Predict (-1 is an Anomaly, 1 is Normal)
    predictions = model.predict(scaled_test_features)
    
    # Get the raw distance score
    raw_scores = model.decision_function(scaled_test_features)

    # ==========================================
    # CONFIDENCE SCORE & RISK LEVEL LOGIC
    # ==========================================
    # Convert raw score to a 0.0 - 1.0 confidence probability
    # Positive raw score (Normal) -> close to 0.0
    # Negative raw score (Anomaly) -> close to 1.0
    confidence_scores = 1 / (1 + np.exp(raw_scores))
    
    # Create the Risk Level tags for the frontend
    conditions = [
        (confidence_scores < 0.40),
        (confidence_scores >= 0.40) & (confidence_scores < 0.75),
        (confidence_scores >= 0.75)
    ]
    choices = ['Low', 'Medium', 'High']
    risk_levels = np.select(conditions, choices, default='Unknown')
    # ==========================================

    # Add all this amazing data back to the dataframe
    df_test['AI_Decision'] = predictions
    df_test['AI_Decision'] = df_test['AI_Decision'].map({1: 'Normal', -1: 'ANOMALY'})
    df_test['Raw_Score'] = np.round(raw_scores, 4)
    df_test['Confidence_Score'] = np.round(confidence_scores, 4) # 0 to 1 score
    df_test['Risk_Level'] = risk_levels # High, Medium, Low

    print("\n" + "="*40)
    print("      DETECTION & SCORING REPORT")
    print("="*40)
    
    high_count = (df_test['Risk_Level'] == 'High').sum()
    med_count = (df_test['Risk_Level'] == 'Medium').sum()
    low_count = (df_test['Risk_Level'] == 'Low').sum()
    
    print(f"Total time-steps analyzed: {len(df_test)}")
    print(f"🟢 Low Risk (Normal):       {low_count}")
    print(f"🟡 Medium Risk (Suspicious):{med_count}")
    print(f"🔴 High Risk (Definite Attack): {high_count}")
    
    # Save the ENTIRE dataset with scores for the frontend
    feed_file_path = '../data/dashboard_feed.csv'
    df_test.to_csv(feed_file_path, index=False)
    
    print("\n[+] DASHBOARD FEED CREATED!")
    print(f"All data points, confidence scores, and risk levels saved to: {feed_file_path}")
    print("Tell Arisha to point her frontend code at this file.")
    print("="*40)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    detect_anomalies()