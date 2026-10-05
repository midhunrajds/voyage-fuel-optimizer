"""Vessel-holdout validation for the Voyage Fuel Optimizer.

Purpose:
    Test whether the model generalises to vessels that were not represented
    in the training set. This is a stronger portfolio validation than a
    random row split when multiple observations belong to the same vessel.

The script deliberately does not use ship_id as a predictive feature.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "ship_fuel_efficiency.csv"

TARGET = "fuel_consumption"
GROUP = "ship_id"
CAT_COLS = [
    "ship_type",
    "route_id",
    "fuel_type",
    "weather_conditions",
    "month",
]
NUM_COLS = ["distance", "engine_efficiency"]
FEATURES = CAT_COLS + NUM_COLS


def build_pipeline() -> Pipeline:
    preprocess = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_COLS),
            ("num", "passthrough", NUM_COLS),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocess", preprocess),
            (
                "model",
                RandomForestRegressor(
                    n_estimators=300,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def main() -> None:
    df = pd.read_csv(DATA_PATH).dropna(subset=FEATURES + [TARGET, GROUP]).copy()

    splitter = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=42)
    train_idx, test_idx = next(splitter.split(df, groups=df[GROUP]))

    train = df.iloc[train_idx].copy()
    test = df.iloc[test_idx].copy()

    model = build_pipeline()
    model.fit(train[FEATURES], train[TARGET])

    predictions = model.predict(test[FEATURES])

    mae = mean_absolute_error(test[TARGET], predictions)
    rmse = np.sqrt(mean_squared_error(test[TARGET], predictions))
    r2 = r2_score(test[TARGET], predictions)

    # A simple training-set mean is included as a transparent reference.
    baseline_pred = np.full(len(test), train[TARGET].mean())
    baseline_mae = mean_absolute_error(test[TARGET], baseline_pred)
    baseline_rmse = np.sqrt(mean_squared_error(test[TARGET], baseline_pred))
    baseline_r2 = r2_score(test[TARGET], baseline_pred)

    print("Vessel-holdout validation")
    print("=" * 28)
    print(f"Training rows:       {len(train):,}")
    print(f"Test rows:           {len(test):,}")
    print(f"Training vessels:    {train[GROUP].nunique():,}")
    print(f"Held-out vessels:    {test[GROUP].nunique():,}")
    print()
    print("Random Forest")
    print(f"MAE:                 {mae:,.2f} L")
    print(f"RMSE:                {rmse:,.2f} L")
    print(f"R²:                  {r2:.4f}")
    print()
    print("Mean baseline")
    print(f"MAE:                 {baseline_mae:,.2f} L")
    print(f"RMSE:                {baseline_rmse:,.2f} L")
    print(f"R²:                  {baseline_r2:.4f}")
    print()
    print(
        "Interpretation: performance on unseen vessels is the key result. "
        "Do not compare it directly with the original random-split score "
        "without noting the different validation design."
    )


if __name__ == "__main__":
    main()
