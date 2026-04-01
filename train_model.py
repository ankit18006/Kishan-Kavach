import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

data = {
    "temperature": [20,25,30,35,28,32,22,26],
    "humidity": [50,60,80,90,70,85,55,65],
    "gas": [100,200,400,600,300,500,150,250],
    "spoilage": [0,1,2,2,1,2,0,1]
}

df = pd.DataFrame(data)

X = df[["temperature","humidity","gas"]]
y = df["spoilage"]

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "spoilage_model.pkl")

print("Model trained")
