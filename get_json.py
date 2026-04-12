import pandas as pd

# Load your clean data
df = pd.read_csv('BATADAL_Train_1.csv')

# Drop the text columns just like we did in training
columns_to_drop = ['DATETIME', 'ATT_FLAG', 'label']
for col in columns_to_drop:
    if col in df.columns:
        df = df.drop(col, axis=1)

# Grab the very first row (which we know is normal) and turn it into JSON!
perfect_normal_json = df.iloc[0].to_json()

print("COPY THIS ENTIRE JSON BLOCK:")
print(perfect_normal_json)