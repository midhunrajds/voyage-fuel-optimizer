import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# Load data
df = pd.read_csv("data/ship_fuel_efficiency.csv")

target = "fuel_consumption"
df = df.dropna(subset=[target])

# Optional: simple outlier filter on target
Q1 = df[target].quantile(0.25)
Q3 = df[target].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
df = df[(df[target] >= lower) & (df[target] <= upper)]
df = df.reset_index(drop=True)

# Features
cat_cols = ["ship_type", "route_id", "fuel_type", "weather_conditions", "month"]
num_cols = ["distance", "engine_efficiency"]

X = df[cat_cols + num_cols]
y = df[target]

# Preprocessing
preprocess = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", "passthrough", num_cols),
    ]
)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(n_estimators=300, random_state=42)

pipe = Pipeline(steps=[
    ("preprocess", preprocess),
    ("model", model)
])

pipe.fit(X_train, y_train)

# Evaluate
y_pred_test = pipe.predict(X_test)
mae_test = mean_absolute_error(y_test, y_pred_test)
rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
r2_test = r2_score(y_test, y_pred_test)

print("Test set performance:")
print(f"MAE:  {mae_test:.2f}")
print(f"RMSE: {rmse_test:.2f}")
print(f"R²:   {r2_test:.4f}")

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(pipe, "models/fuel_model_rf_v1.joblib")
print("Model saved to models/fuel_model_rf_v1.joblib")
