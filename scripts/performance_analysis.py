"""Grouped out-of-fold voyage performance analysis.

This script estimates expected fuel for each observation without training on
that observation or on other observations from the same vessel fold.

It is a portfolio analysis, not a production vessel-performance methodology.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "ship_fuel_efficiency.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "voyage_performance_oof.csv"

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
        [
            ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_COLS),
            ("num", "passthrough", NUM_COLS),
        ]
    )
    return Pipeline(
        [
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
    df = pd.read_csv(DATA_PATH).dropna(
        subset=FEATURES + [TARGET, GROUP]
    ).copy()

    predictions = np.full(len(df), np.nan)
    splitter = GroupKFold(n_splits=5)

    for train_idx, test_idx in splitter.split(
        df[FEATURES], df[TARGET], groups=df[GROUP]
    ):
        model = build_pipeline()
        model.fit(df.iloc[train_idx][FEATURES], df.iloc[train_idx][TARGET])
        predictions[test_idx] = model.predict(df.iloc[test_idx][FEATURES])

    result = df.copy()
    result["expected_fuel"] = predictions
    result["fuel_deviation"] = result[TARGET] - result["expected_fuel"]
    result["fuel_deviation_pct"] = (
        result["fuel_deviation"]
        / result["expected_fuel"].replace(0, np.nan)
    ) * 100
    result["absolute_error"] = result["fuel_deviation"].abs()

    OUTPUT_DIR.mkdir(exist_ok=True)
    result.to_csv(OUTPUT_PATH, index=False)

    mae = mean_absolute_error(result[TARGET], result["expected_fuel"])
    rmse = np.sqrt(mean_squared_error(result[TARGET], result["expected_fuel"]))
    r2 = r2_score(result[TARGET], result["expected_fuel"])

    print("Grouped out-of-fold voyage performance analysis")
    print("=" * 48)
    print(f"Rows analysed:       {len(result):,}")
    print(f"Vessels:             {result[GROUP].nunique():,}")
    print(f"MAE:                 {mae:,.2f} L")
    print(f"RMSE:                {rmse:,.2f} L")
    print(f"R²:                  {r2:.4f}")
    print()
    print("Performance deviation")
    print(f"Mean deviation:      {result['fuel_deviation'].mean():,.2f} L")
    print(f"Median deviation:    {result['fuel_deviation'].median():,.2f} L")
    print(f"Mean absolute deviation: {result['absolute_error'].mean():,.2f} L")
    print()
    print(f"Detailed output:      {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
