import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Voyage Fuel Optimizer",
    page_icon="🚢",
    layout="wide"
)

st.title("🚢 Voyage Fuel Optimizer")
st.markdown(
    "Find fuel‑optimal speeds for a given voyage using a trained ML model and cubic speed–fuel scaling."
)

# Resolve paths relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "fuel_model_rf_v1.joblib"
DATA_DIR = BASE_DIR / "data"

# Load model
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

feature_cols = [
    "ship_type", "route_id", "fuel_type", "weather_conditions", "month",
    "distance", "engine_efficiency"
]

# Hardcoded metadata (you can adjust later)
available_ship_types = ["Oil Service Boat"]
available_fuel_types = ["HFO"]
reference_speed = 12.0  # v_ref for cubic scaling

# Sidebar: voyage inputs
st.sidebar.header("Voyage inputs")

ship_type = st.sidebar.selectbox(
    "Ship type",
    options=available_ship_types,
    index=0
)

fuel_type = st.sidebar.selectbox(
    "Fuel type",
    options=available_fuel_types,
    index=0
)

route_id = st.sidebar.text_input(
    "Route (e.g., Port Harcourt-Lagos)",
    value="Port Harcourt-Lagos"
)

weather = st.sidebar.selectbox(
    "Weather conditions",
    options=["Calm", "Moderate", "Stormy"],
    index=1
)

month = st.sidebar.selectbox(
    "Month",
    options=[
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ],
    index=1
)

distance = st.sidebar.number_input(
    "Distance (units)",
    min_value=1.0,
    value=128.52,
    step=0.01
)

engine_efficiency = st.sidebar.number_input(
    "Engine efficiency",
    min_value=0.0,
    max_value=100.0,
    value=92.98,
    step=0.01
)

eta_max_hours = st.sidebar.number_input(
    "Max travel time (ETA, hours)",
    min_value=1.0,
    value=12.0,
    step=0.5
)

# Optimizer logic
st.header("Optimization results")

# Speed range
min_speed = 8.0
max_speed = 18.0
speeds = np.linspace(min_speed, max_speed, 41)

# Base feature row
base_row = pd.DataFrame([{
    "ship_type": ship_type,
    "route_id": route_id,
    "fuel_type": fuel_type,
    "weather_conditions": weather,
    "month": month,
    "distance": distance,
    "engine_efficiency": engine_efficiency,
}])

for c in ["ship_type", "route_id", "fuel_type", "weather_conditions", "month"]:
    base_row[c] = base_row[c].astype(str)
base_row["distance"] = base_row["distance"].astype(float)
base_row["engine_efficiency"] = base_row["engine_efficiency"].astype(float)

# Base fuel/day from model
fuel_base = model.predict(base_row[feature_cols])[0]

results = []
for sp in speeds:
    time_hours = distance / sp
    if time_hours > eta_max_hours:
        continue
    # Cubic scaling
    fuel_per_day = fuel_base * (sp / reference_speed) ** 3
    total_fuel = fuel_per_day * (time_hours / 24.0)
    results.append({
        "speed": sp,
        "time_hours": time_hours,
        "fuel_per_day": fuel_per_day,
        "total_fuel": total_fuel
    })

res_df = pd.DataFrame(results)

if res_df.empty:
    st.warning("No feasible speed found that meets the ETA constraint with the given inputs.")
else:
    opt = res_df.loc[res_df["total_fuel"].idxmin()]
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Optimal speed", f"{opt['speed']:.2f}")
    with col2:
        st.metric("Travel time", f"{opt['time_hours']:.2f} h")
    with col3:
        st.metric("Fuel/day", f"{opt['fuel_per_day']:.2f}")
    with col4:
        st.metric("Total fuel", f"{opt['total_fuel']:.2f}")
    
    # Plot: total fuel vs speed
    st.subheader("Total fuel vs speed")
    fig1, ax1 = plt.subplots()
    sns.lineplot(data=res_df, x="speed", y="total_fuel", ax=ax1)
    ax1.axvline(opt["speed"], color="red", linestyle="--", label=f"Optimal ≈ {opt['speed']:.2f}")
    ax1.set_xlabel("Speed (units/hour)")
    ax1.set_ylabel("Total fuel (units)")
    ax1.set_title("Voyage fuel vs speed (cubic scaling)")
    ax1.legend()
    st.pyplot(fig1)
    
    # Plot: fuel/day vs speed
    st.subheader("Fuel/day vs speed")
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=res_df, x="speed", y="fuel_per_day", ax=ax2)
    ax2.axvline(reference_speed, color="gray", linestyle=":", label=f"Reference speed = {reference_speed:.0f}")
    ax2.axvline(opt["speed"], color="red", linestyle="--", label=f"Optimal ≈ {opt['speed']:.2f}")
    ax2.set_xlabel("Speed (units/hour)")
    ax2.set_ylabel("Fuel/day (units)")
    ax2.set_title("Fuel/day vs speed (cubic scaling)")
    ax2.legend()
    st.pyplot(fig2)
    
    # Optional: sample table
    st.subheader("Sample of computed values")
    st.dataframe(res_df[["speed", "time_hours", "fuel_per_day", "total_fuel"]].round(2))

# Footer
st.markdown("---")
st.markdown(
    "Built as part of the [Voyage Fuel Optimizer](https://github.com/midhunrajds/voyage-fuel-optimizer) project."
)
