import pandas as pd
import numpy as np
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import joblib
import os

def train_process_model():
    print("Loading BATADAL dataset...")
    data_path = '../data/batadal_train.csv'
    df = pd.read_csv(data_path)

    # BULLETPROOF FIX: Strip spaces and force all columns to UPPERCASE
    df.columns = df.columns.str.strip().str.upper()

    # Drop non-sensor columns
    columns_to_drop = ['DATETIME', 'ATT_FLAG', 'ATTACK'] 
    features = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

    print("Scaling the sensor data...")
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    print("Training One-Class SVM...")
    ocsvm_model = OneClassSVM(kernel='rbf', gamma='scale', nu=0.05)
    ocsvm_model.fit(scaled_features)

    print("Saving the trained model and scaler...")
    joblib.dump(ocsvm_model, '../models/batadal_ocsvm.pkl')
    joblib.dump(scaler, '../models/batadal_scaler.pkl')
    
    print("Training complete! Check your models folder.")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    train_process_model()