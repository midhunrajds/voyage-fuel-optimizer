# Model Notes — Voyage Fuel Optimizer

## What this model is for

This model is part of a portfolio proof of concept.

The aim is to show that I can take a simple maritime dataset, build a predictive model, question the validation approach, and use the result as a starting point for a vessel-performance analysis.

It is **not** a production fuel-consumption model.

## Target

`fuel_consumption` as defined by the source dataset.

For this project it is treated as the fuel-consumption value attached to each voyage record. I have not converted it into fuel/day or fuel/nm because that would require a source definition that is not available in the project documentation.

## Inputs used by the model

Categorical:

- `ship_type`
- `route_id`
- `fuel_type`
- `weather_conditions`
- `month`

Numeric:

- `distance`
- `engine_efficiency`

`ship_id` is retained for inspection and validation grouping. It is not used as a predictive feature.

## Model

The main analysis uses a Random Forest Regressor with 300 trees inside a scikit-learn preprocessing pipeline.

The Streamlit application uses the same feature design but retrains a smaller 100-tree model at startup.

The important point is that the model is deliberately fairly simple. The purpose of the project is to demonstrate a sensible workflow rather than to maximise model complexity.

## First result

The original random row-level split produced approximately:

- R²: 0.93
- MAE: 342 L
- RMSE: 461 L

I kept this result because it shows where the project started.

I do not use it as the main evidence of generalisation.

## Why I changed the validation

The dataset contains repeated observations from individual vessels.

If rows from the same vessel appear in both training and test sets, the model can benefit from patterns associated with that vessel. That does not necessarily tell me how it will behave for a vessel that was not represented in training.

I therefore added:

- 5-fold GroupKFold analysis using `ship_id`;
- a separate held-out-vessel test.

## Current validation results

### Grouped out-of-fold

| Metric | Result |
|---|---:|
| MAE | 610.52 L |
| RMSE | 1,071.39 L |
| R² | 0.9520 |

### Held-out vessels

The model was trained on 96 vessels and tested on 24 vessels that were completely excluded from training.

| Metric | Result |
|---|---:|
| MAE | 790.97 L |
| RMSE | 1,330.34 L |
| R² | 0.9470 |

A simple mean baseline on those 24 vessels produced MAE 4,148.16 L, RMSE 5,971.64 L and R² -0.0684.

The result is encouraging for this dataset, but it is not evidence that the model is ready for commercial use.

## How expected fuel is used

The grouped out-of-fold predictions are treated as an estimate of expected fuel for each observation.

I calculate:

`fuel_deviation = actual fuel - expected fuel`

and:

`fuel_deviation_pct = fuel_deviation / expected fuel × 100`

The purpose is to create a simple screening signal.

A positive deviation means the observed fuel consumption is higher than the model expected.

It does **not** automatically mean the vessel has a technical problem. An investigation would need the operating context and the quality of the underlying data.

## Speed scenario assumption

The application contains a separate scenario calculation for speed and ETA.

It derives a reference fuel rate from the model prediction and applies a cubic relationship to speed:

`F_day(v) = F_day(v_ref) × (v / v_ref)^3`

This is a transparent assumption used to explore a scenario.

It is not a vessel-specific resistance curve, hydrodynamic model or validated speed-power relationship.

## Main limitations

- public/non-operational dataset;
- relatively small dataset;
- no live AIS;
- no high-frequency machinery data;
- no measured engine load/RPM;
- no draft/trim/displacement;
- no measured wind/wave/current data;
- no vessel-specific speed-power curve;
- no hull/propeller condition;
- no bunker reconciliation;
- no uncertainty estimate;
- no production monitoring;
- no true temporal backtesting because the available dataset does not provide a suitable date/time field.

## What a real implementation would need

With real vessel data, I would first improve the data rather than immediately change the algorithm.

I would want to establish:

- reliable timestamps;
- vessel and voyage/segment identifiers;
- clearly defined fuel measurements;
- AIS and speed information;
- draft/trim;
- engine load and RPM;
- weather and ocean conditions;
- vessel-specific performance information;
- data-quality rules and source definitions.

Validation would then need to consider the actual use case. Depending on the question, that could include vessel holdout, time-based testing and route or operating-condition holdout.

Only after those foundations were in place would I consider whether a more complex model was justified.
