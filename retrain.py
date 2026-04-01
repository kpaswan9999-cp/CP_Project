import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import warnings
warnings.filterwarnings('ignore')

# 1. Load the original dataset
df = pd.read_csv(r"C:\Users\kpasw\OneDrive\Desktop\CP 2\5g_network_data.csv")

# 2. Select only the necessary features and drop NaNs
features = [
    "Signal Strength (dBm)",
    "Download Speed (Mbps)",
    "Latency (ms)",
    "Jitter (ms)",
    "VoNR Enabled",
    "Dropped Connection"
]
df = df.dropna(subset=features)

# 3. Compute realistic quality score
# Speed: 0-1000 Mbps. Let's cap at 500 for scaling.
speed_score = np.clip(df["Download Speed (Mbps)"] / 100, 0, 5) # Up to 5 points
# Latency: < 20 gets 5, > 100 gets 0
lat_score = np.clip((100 - df["Latency (ms)"]) / 16, 0, 5) # Up to 5 points
# Signal: > -70 gets 5, < -110 gets 0
sig_score = np.clip((df["Signal Strength (dBm)"] + 110) / 8, 0, 5) # Up to 5 points
# Congestion, Jitter, Drop
jitter_penalty = df["Jitter (ms)"] * 0.2
drop_penalty = df["Dropped Connection"].astype(int) * 3

total_score = speed_score * 2 + lat_score + sig_score * 1.5 - jitter_penalty - drop_penalty

# Bins for absolute real-world mapping (max ~ 22.5)
# < 6 = 0 (1 in UI: Critical Poor)
# 6-9 = 1 (2 in UI: Poor Quality)
# 9-13 = 2 (3 in UI: Moderate / Stable)
# 13-17 = 3 (4 in UI: Very Good)
# > 17 = 4 (5 in UI: Excellent)
df["New Quality"] = pd.cut(total_score, bins=[-np.inf, 6, 9, 13, 17, np.inf], labels=[0, 1, 2, 3, 4]).astype(int)

# Check the test case score
test_speed_score = min(400/100, 5) # 4
test_lat_score = min((100 - 15)/16, 5) # 5
test_sig_score = min((-65 + 110)/8, 5) # 5
test_total = 4*2 + 5 + 5*1.5 - 3*0.2 - 0
# 8 + 5 + 7.5 - 0.6 = 19.9

# 4. Filter x and y
x = df[features].copy()
y = df["New Quality"]

# 5. Encoding
le = LabelEncoder()
x['VoNR Enabled'] = le.fit_transform(x['VoNR Enabled'])
x['Dropped Connection'] = le.fit_transform(x['Dropped Connection'])

# 6. Train model
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)
model.fit(x_train, y_train)

# 7. Evaluate on User Test Case 2
feats2 = np.array([[-85.0, 150.0, 40.0, 8.0, 1, 0]])
pred = model.predict(feats2)[0]
print("Test Case 2 Prediction (0-4):", pred)

# 8. Save
pickle.dump(model, open("model.pkl", "wb"))
print("Model retrained and saved to model.pkl successfully.")
