# Model Card — Voyage Fuel Optimizer

## Intended use

Portfolio demonstration of a maritime predictive-analytics workflow using a public dataset.

## Target

`fuel_consumption` as defined by the source dataset. The project currently treats this as fuel consumed for a voyage record.

## Inputs

Categorical:
- ship_type
- route_id
- fuel_type
- weather_conditions
- month

Numeric:
- distance
- engine_efficiency

`ship_id` is retained for data inspection and validation grouping but is not used as a model feature.

## Model

Random Forest Regressor, 300 trees, inside a scikit-learn preprocessing pipeline.

The Streamlit application uses the same feature design but retrains a smaller 100-tree model at startup to avoid dependence on a serialized model artifact.

## Reported baseline performance

The original project reports approximately R² 0.93, MAE 342 L and RMSE 461 L from a random row-level train/test split.

These results are not sufficient evidence of production performance because multiple observations belong to the same vessel. Random splitting can therefore place observations from the same vessel in both training and test sets.

## Stronger validation

The repository now includes `scripts/validate_generalisation.py`, which performs a **vessel-holdout split** using `ship_id` only as a grouping variable. The model is trained on one set of vessels and evaluated on previously unseen vessels.

A simple training-set mean is also reported as a transparent baseline.

This validation is more relevant to the question:

> Can the model generalise to a vessel that was not represented in the training data?

The resulting vessel-holdout metrics should be reported alongside the original random-split metrics, not substituted silently.

## Optimisation assumption

The application derives an implied reference fuel rate from the ML-predicted voyage fuel and supplied distance/reference speed, then applies a cubic speed relationship.

This is a scenario assumption, not a vessel-specific hydrodynamic model.

## Key limitations

- public/non-operational dataset;
- no live AIS;
- no time-series engine data;
- no RPM/load curve;
- no draft/trim/displacement;
- no wind/wave/current correction;
- no hull/propeller fouling state;
- no bunker reconciliation;
- no vessel-specific speed-power curve;
- no uncertainty estimation;
- no production monitoring or alerting;
- no true date/time field, so genuine temporal backtesting is not currently possible.

## Production path

A production-grade solution should use vessel-specific baselines, time-aware and vessel/route holdout validation, data-quality controls, AIS/weather/engine integration, uncertainty monitoring, model drift detection, explainable recommendations and operator approval workflows.
