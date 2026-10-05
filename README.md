# Voyage Fuel Optimizer — Maritime Fuel Consumption & Voyage Decision-Support POC

A public-data proof of concept demonstrating how a maritime professional can combine machine learning, vessel-domain knowledge and scenario analysis to explore fuel-consumption and voyage-speed decisions.

> **Important:** This is a data-science portfolio project, not a production vessel-performance system. The dataset is public/synthetic-style tabular voyage data and does not represent live operational data from a specific vessel.

## 🚀 Live App

**Try the interactive Streamlit application:** [Open Voyage Fuel Optimizer](https://voyage-fuel-optimizer-abjnte8lhjkkua6ebpaxle.streamlit.app/)

The app lets you enter a voyage scenario, estimate fuel consumption, and explore speed/ETA sensitivity. The result is a portfolio proof of concept and should not be interpreted as a production vessel-performance recommendation.

## Problem

Ship operators continuously balance fuel consumption, voyage time and schedule requirements. A useful decision-support workflow should be able to:

- estimate fuel consumption for a voyage scenario;
- test how speed and ETA constraints affect a voyage;
- expose the assumptions behind an optimisation result; and
- identify what additional operational data would be required before deployment.

## Dataset

The project uses `data/ship_fuel_efficiency.csv` with 1,440 records and fields including:

- vessel/ship identifier and ship type
- route
- month
- distance
- fuel type
- fuel consumption
- CO₂ emissions
- weather condition
- engine efficiency

The current model does **not** use `ship_id` as a predictive feature.

## Modelling approach

The baseline model is a scikit-learn pipeline containing:

- one-hot encoding for categorical variables;
- passthrough numeric variables;
- Random Forest Regression with 300 trees.

The current target is `fuel_consumption` **per voyage record**. It should not be interpreted as a directly observed fuel-per-day or fuel-per-nautical-mile measure unless the source dataset defines it that way.

The original model evaluation reports approximately:

- R²: 0.93
- MAE: 342 L
- RMSE: 461 L

These figures are useful as a portfolio baseline, but they should not be interpreted as production-grade vessel-performance accuracy. Random train/test splitting can overstate generalisation when observations are related by vessel, route or repeated operating conditions.

## Validation strategy

The repository now includes a stronger validation path in `scripts/validate_generalisation.py`.

Instead of randomly splitting individual rows, the validation script holds out entire vessels using `ship_id` as a **grouping variable only**. The model therefore has to predict observations from vessels it did not see during training.

The script also reports a simple training-set mean baseline.

This is an important distinction for a vessel-performance portfolio project:

**random row split → “Can the model fit similar observations?”**

**vessel holdout → “Can the model generalise to an unseen vessel?”**

The vessel-holdout result should be reported alongside the original random-split result rather than silently replacing it.

## Voyage-speed scenario analysis

The application separates two concepts:

1. **ML estimate:** predicted fuel consumption for the supplied voyage scenario.
2. **Speed sensitivity:** a transparent physics-inspired cubic relationship used only as a scenario assumption.

For a reference speed (v_ref), the model-predicted voyage fuel is converted to an implied reference fuel rate using the supplied distance and reference speed. The rate is then scaled as:

`F_day(v) = F_day(v_ref) × (v / v_ref)^3`

and total voyage fuel is calculated from voyage time.

This makes the units internally consistent, but the result remains an **assumption-driven scenario estimate**. The dataset does not establish a vessel-specific speed-power curve.

## Example

For the example Port Harcourt–Lagos scenario with a 12-hour ETA constraint, the earlier notebook produced an optimum around 10.75 knots and approximately 1,496 L total fuel.

That result should be read as:

> “Under this dataset and the stated cubic speed-scaling assumption, the lowest feasible speed meeting the ETA constraint is approximately 10.75 knots.”

It should **not** be presented as the real optimum operating speed of a commercial vessel.

## Why this matters in real vessel-performance work

A production vessel-performance solution would normally combine sources such as:

- noon reports / daily reports;
- AIS position and speed data;
- engine and machinery parameters;
- RPM and load;
- draft, displacement and trim;
- wind, waves, currents and weather routing;
- hull/propeller condition and fouling;
- bunker delivery and consumption records;
- vessel-specific speed-power curves;
- voyage plan, ETA and charter-party constraints.

A production system would also need vessel-specific baselines, data-quality controls, anomaly detection, model monitoring, explainability, uncertainty estimates and operational workflows for recommendations.

## Portfolio value

This project demonstrates an end-to-end workflow:

**maritime problem → data preparation → predictive modelling → validation design → scenario analysis → visual decision support → production-gap assessment**

The most important capability demonstrated is not the model score alone. It is the ability to connect a machine-learning result to a maritime operational question while clearly identifying assumptions and limitations.

## Repository structure

- `data/` — public project dataset
- `notebooks/01_eda_and_model_selection.ipynb` — EDA and model comparison
- `notebooks/02_voyage_optimizer.ipynb` — speed/ETA scenario analysis
- `models/` — trained model artifact
- `app/streamlit_app.py` — interactive scenario application
- `retrain_model.py` — model training script
- `scripts/validate_generalisation.py` — vessel-holdout validation
- `docs/model_card.md` — modelling assumptions, limitations and production gaps

## Running locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

To run the stronger validation:

```bash
python scripts/validate_generalisation.py
```

## Future development

The next technical milestones are deliberately focused on evidence rather than adding complexity:

1. run and document the vessel-holdout results;
2. add uncertainty/error analysis;
3. add route-holdout validation;
4. normalise fuel metrics by distance/time where source definitions permit;
5. incorporate AIS and weather data;
6. develop vessel-specific speed-power relationships;
7. add emissions and cost optimisation;
8. build data-quality and anomaly monitoring; and
9. design a fleet-level dashboard and recommendation workflow.

## About

Independent maritime data-science project by Midhun Raj, combining marine engineering and technical-superintendent experience with data analytics, machine learning and maritime digitalisation.

GitHub: https://github.com/midhunrajds
