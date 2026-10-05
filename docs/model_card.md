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

`ship_id` is retained for data inspection but is not used as a model feature.

## Model

Random Forest Regressor, 300 trees, inside a scikit-learn preprocessing pipeline.

## Reported baseline performance

The existing project reports approximately R² 0.93, MAE 342 L and RMSE 461 L.

These results are not sufficient evidence of production performance because the current evaluation uses a random split and the dataset may contain correlated observations across vessels/routes.

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
- no production monitoring or alerting.

## Production path

A production-grade solution should use vessel-specific baselines, time-aware and vessel/route holdout validation, data-quality controls, AIS/weather/engine integration, uncertainty monitoring, model drift detection, explainable recommendations and operator approval workflows.
