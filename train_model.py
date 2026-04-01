import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# 🔥 DB connect
conn = sqlite3.connect("database.db")

df = pd.read_sql_query("""
SELECT temperature, humidity, gas, spoilage
FROM sensor_data
WHERE spoilage IS NOT NULL
""", conn)

# Convert labels
df['spoilage'] = df['spoilage'].map({
    "LOW": 0,
    "MEDIUM": 1,
    "HIGH": 2
})

# Features
X = df[['temperature', 'humidity', 'gas']]
y = df['spoilage']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🔥 MODEL
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5
)

model.fit(X_train, y_train)

# Accuracy check
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)

print(f"🔥 Accuracy: {acc*100:.2f}%")

# Save
joblib.dump(model, "spoilage_model.pkl")
