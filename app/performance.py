import numpy as np
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


CAT_COLS = [
    "ship_type",
    "route_id",
    "fuel_type",
    "weather_conditions",
    "month",
]
NUM_COLS = ["distance", "engine_efficiency"]
FEATURES = CAT_COLS + NUM_COLS
TARGET = "fuel_consumption"
GROUP = "ship_id"


def _build_pipeline():
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


@st.cache_data
def grouped_oof_analysis(dataset):
    df = dataset.dropna(subset=FEATURES + [TARGET, GROUP]).copy()
    predictions = np.full(len(df), np.nan)
    splitter = GroupKFold(n_splits=5)

    for train_idx, test_idx in splitter.split(
        df[FEATURES], df[TARGET], groups=df[GROUP]
    ):
        model = _build_pipeline()
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

    metrics = {
        "mae": mean_absolute_error(result[TARGET], result["expected_fuel"]),
        "rmse": np.sqrt(
            mean_squared_error(result[TARGET], result["expected_fuel"])
        ),
        "r2": r2_score(result[TARGET], result["expected_fuel"]),
        "vessels": int(result[GROUP].nunique()),
        "rows": int(len(result)),
    }
    return result, metrics
