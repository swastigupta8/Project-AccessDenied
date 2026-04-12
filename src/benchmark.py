import pandas as pd
import numpy as np
import joblib
import os
from sklearn.metrics import classification_report

def run_full_matrix_benchmark():
    # 1. Load the Brain and the Test Data
    print("Loading AI Brain and Test Dataset...")
    model = joblib.load('../models/batadal_ocsvm.pkl')
    scaler = joblib.load('../models/batadal_scaler.pkl')

    df_test = pd.read_csv('../data/batadal_test.csv')
    df_test.columns = df_test.columns.str.strip().str.upper()

    # 2. Extract Reality (1 is Attack, everything else is Normal)
    y_true = df_test['ATT_FLAG'].apply(lambda x: 'Actual_Normal' if x != 1 else 'Actual_Attack')

    # 3. Blind the AI (Remove labels)
    columns_to_drop = ['DATETIME', 'ATT_FLAG', 'ATTACK']
    features_test = df_test.drop(columns=[col for col in columns_to_drop if col in df_test.columns])

    # 4. AI Analysis
    print("AI is calculating risk levels for the full matrix...")
    scaled_features = scaler.transform(features_test)
    raw_scores = model.decision_function(scaled_features)
    
    # Calculate 0-1 Confidence
    confidence_scores = 1 / (1 + np.exp(raw_scores))
    
    # Categorize into the 3 Risk Levels
    conditions = [
        (confidence_scores < 0.40),
        (confidence_scores >= 0.40) & (confidence_scores < 0.75),
        (confidence_scores >= 0.75)
    ]
    choices = ['Low', 'Medium', 'High']
    risk_levels = np.select(conditions, choices, default='Unknown')

    # 5. Create the Full Matrix (Cross-tabulation)
    results = pd.DataFrame({'Reality': y_true, 'AI_Perception': risk_levels})
    full_matrix = pd.crosstab(results['AI_Perception'], results['Reality'])
    
    # Ensure all levels (Low, Medium, High) are present in the final file
    for level in ['Low', 'Medium', 'High']:
        if level not in full_matrix.index:
            full_matrix.loc[level] = 0
    full_matrix = full_matrix.reindex(['Low', 'Medium', 'High'])

    # 6. Save the FULL MATRIX for the Frontend
    full_matrix.to_csv('../data/full_risk_matrix.csv')

    # 7. Print Report to Terminal
    print("\n" + "="*50)
    print("      FULL RISK-LEVEL CONFUSION MATRIX")
    print("="*50)
    print(full_matrix)
    print("-" * 50)
    
    # Simple summary for your presentation slides
    total_attacks = (results['Reality'] == 'Actual_Attack').sum()
    caught = full_matrix.loc['High', 'Actual_Attack'] + full_matrix.loc['Medium', 'Actual_Attack']
    
    print(f"Total Actual Attacks: {total_attacks}")
    print(f"Total AI Detections:  {caught} (High + Medium)")
    print(f"Detection Rate:       {(caught/total_attacks):.2%}")
    print("="*50)
    print("Success! 'full_risk_matrix.csv' is ready for the frontend.")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_full_matrix_benchmark()