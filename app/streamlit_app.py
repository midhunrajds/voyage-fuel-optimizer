import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Voyage Fuel Optimizer", page_icon="🚢", layout="wide")

st.title("🚢 Voyage Fuel Optimizer")
st.caption(
    "Public-data proof of concept: ML fuel estimate + transparent speed/ETA scenario analysis. "
    "Not a production vessel-performance model."
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "ship_fuel_efficiency.csv"

feature_cols = [
    "ship_type", "route_id", "fuel_type", "weather_conditions",
    "month", "distance", "engine_efficiency"
]
cat_cols = ["ship_type", "route_id", "fuel_type", "weather_conditions", "month"]
num_cols = ["distance", "engine_efficiency"]

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    required = feature_cols + ["fuel_consumption"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    return df.dropna(subset=required).copy()

@st.cache_resource
def build_model(dataset):
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder

    preprocess = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ("num", "passthrough", num_cols),
        ]
    )
    pipeline = Pipeline([
        ("preprocess", preprocess),
        ("model", RandomForestRegressor(
            n_estimators=100, random_state=42, n_jobs=-1
        )),
    ])
    pipeline.fit(dataset[feature_cols], dataset["fuel_consumption"])
    return pipeline

dataset = load_data()
model = build_model(dataset)
st.caption("Model status: trained at app startup from the repository dataset")

st.sidebar.header("Voyage inputs")

ship_type = st.sidebar.selectbox("Ship type", sorted(dataset["ship_type"].unique()))
fuel_type = st.sidebar.selectbox("Fuel type", sorted(dataset["fuel_type"].unique()))
route_id = st.sidebar.selectbox("Route", sorted(dataset["route_id"].unique()))
weather = st.sidebar.selectbox("Weather conditions", sorted(dataset["weather_conditions"].unique()))
month = st.sidebar.selectbox("Month", list(dataset["month"].unique()))
distance = st.sidebar.number_input("Distance (nautical miles)", min_value=1.0, value=128.52, step=0.01)
engine_efficiency = st.sidebar.number_input(
    "Engine efficiency (%)", min_value=0.0, max_value=100.0, value=92.98, step=0.01
)
eta_max_hours = st.sidebar.number_input("Maximum voyage time / ETA (hours)", min_value=1.0, value=12.0, step=0.5)
reference_speed = st.sidebar.number_input(
    "Reference speed for scenario scaling (knots)",
    min_value=1.0, value=12.0, step=0.25
)

base_row = pd.DataFrame([{
    "ship_type": ship_type,
    "route_id": route_id,
    "fuel_type": fuel_type,
    "weather_conditions": weather,
    "month": month,
    "distance": float(distance),
    "engine_efficiency": float(engine_efficiency),
}])

predicted_voyage_fuel = float(model.predict(base_row[feature_cols])[0])

# The model predicts voyage-record fuel, not fuel/day. Convert it to an
# implied reference daily rate using the supplied reference speed, then
# apply the cubic relationship as an explicit scenario assumption.
reference_time_hours = distance / reference_speed
reference_fuel_per_day = predicted_voyage_fuel / (reference_time_hours / 24.0)

speeds = np.linspace(8.0, 18.0, 41)
rows = []

for speed in speeds:
    time_hours = distance / speed
    if time_hours <= eta_max_hours:
        fuel_per_day = reference_fuel_per_day * (speed / reference_speed) ** 3
        total_fuel = fuel_per_day * (time_hours / 24.0)
        rows.append({
            "speed": speed,
            "time_hours": time_hours,
            "fuel_per_day": fuel_per_day,
            "total_fuel": total_fuel,
        })

res_df = pd.DataFrame(rows)

st.info(
    f"ML baseline estimate: **{predicted_voyage_fuel:,.0f} L per voyage record**. "
    "The speed curve below is a scenario model built from an assumed cubic relationship."
)

if res_df.empty:
    st.warning("No candidate speed in the selected range satisfies the ETA constraint.")
else:
    opt = res_df.loc[res_df["total_fuel"].idxmin()]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Scenario speed", f"{opt['speed']:.2f} kn")
    c2.metric("Travel time", f"{opt['time_hours']:.2f} h")
    c3.metric("Scenario fuel/day", f"{opt['fuel_per_day']:,.0f} L")
    c4.metric("Scenario total fuel", f"{opt['total_fuel']:,.0f} L")

    st.subheader("Fuel vs speed")
    chart_df = res_df.set_index("speed")[["total_fuel"]]
    st.line_chart(chart_df, y="total_fuel", height=350)

    st.subheader("Scenario table")
    st.dataframe(res_df.round(2), use_container_width=True)

st.warning(
    "Interpretation: this is a portfolio proof of concept. The speed optimisation is not a "
    "validated vessel-specific speed-power model and should not be used for real voyage decisions."
)

st.markdown("---")
st.markdown(
    "Built as part of the [Voyage Fuel Optimizer](https://github.com/midhunrajds/voyage-fuel-optimizer) project."
)
