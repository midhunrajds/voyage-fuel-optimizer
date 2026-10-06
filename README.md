# Voyage Fuel Optimizer — Maritime Fuel & Performance POC

A portfolio project built to show how I would approach a vessel fuel-performance problem using public data, Python and machine learning.

> **This is a proof of concept, not a production vessel-performance system.** I built it because I wanted to connect my marine-engineering and technical-management experience with the data-science skills I have been developing.

## Live app

[Open Voyage Fuel Optimizer](https://voyage-fuel-optimizer-abjnte8lhjkkua6ebpaxle.streamlit.app/)

The app lets you enter a voyage scenario, estimate fuel consumption and explore the effect of speed and ETA assumptions.

The result is intended for portfolio demonstration. It is **not** a recommendation for operating a commercial vessel.

## What I was trying to answer

I started with a simple question:

> **Can I use the information available in a public voyage dataset to estimate fuel consumption reasonably well?**

After building the first model, I had a second question:

> **Does the model still work when it is asked to predict a vessel it has never seen before?**

I then extended the project one step further:

> **Can the prediction be used as an expected value so that actual fuel consumption can be compared with it?**

That led to the current workflow:

**voyage data → fuel prediction → vessel-aware validation → expected fuel → actual vs expected**

## The dataset

The project uses `data/ship_fuel_efficiency.csv`.

It contains:

- 1,440 voyage records
- 120 vessels
- ship type
- route
- month
- distance
- fuel type
- weather condition
- engine efficiency
- fuel consumption
- CO₂ emissions

The source dataset is much simpler than the information normally available in a real vessel-performance environment. That is an important limitation of the project.

`ship_id` is kept for inspection and validation grouping, but it is not used as a model feature.

## What I built

### 1. Initial fuel-consumption model

I used a scikit-learn pipeline with:

- one-hot encoding for categorical variables;
- numeric features passed through;
- Random Forest regression.

The original random row-level split produced approximately:

- **R²: 0.93**
- **MAE: 342 L**
- **RMSE: 461 L**

These numbers are useful as the first result from the project, but I did not want to stop there.

Because the same vessel can appear in multiple rows, a random split can put observations from one vessel into both training and test sets. That can make the model look more general than it really is.

### 2. Vessel-aware validation

I therefore added two additional checks.

**Grouped out-of-fold analysis**

The performance workflow uses 5-fold GroupKFold with `ship_id` as the grouping variable. Each prediction is made by a model that did not train on other observations from that same vessel.

Result:

| Metric | Grouped OOF |
|---|---:|
| MAE | 610.52 L |
| RMSE | 1,071.39 L |
| R² | 0.9520 |

**Held-out-vessel test**

A separate validation script holds out complete vessels:

- 96 vessels for training
- 24 completely unseen vessels for testing

Result:

| Metric | Held-out vessels |
|---|---:|
| MAE | 790.97 L |
| RMSE | 1,330.34 L |
| R² | 0.9470 |

For comparison, a simple mean baseline on those 24 test vessels produced:

- MAE: 4,148.16 L
- RMSE: 5,971.64 L
- R²: -0.0684

The held-out result is encouraging, but I would not describe it as production accuracy. The dataset is still a relatively small public dataset and does not contain the operational information available in a real vessel environment.

## Turning prediction into a performance signal

The next step was to make the project more useful than a single prediction.

For each record, the grouped out-of-fold model produces an **expected fuel** value.

I can then calculate:

**fuel deviation = actual fuel − expected fuel**

and a percentage deviation.

This gives a simple way of asking:

> **Was this observation above or below what the model expected?**

A positive deviation means actual consumption was higher than the model's expected value.

It is only a **screening signal**. It does not prove that a vessel was technically underperforming. A real investigation would need the operating context.

For example, higher fuel consumption could be associated with speed, distance, draft/trim, weather, sea state, current, machinery condition, operational mode or an unusual event.

## Speed and ETA scenario analysis

The Streamlit app also contains a simple speed-sensitivity calculation.

The model prediction is used to derive a reference fuel rate, and that rate is then adjusted using a cubic speed relationship:

`F_day(v) = F_day(v_ref) × (v / v_ref)^3`

I included this because it gives the user a way to explore the relationship between speed, voyage time and fuel.

However, this is an **assumption used for the scenario tool**. The public dataset does not provide a vessel-specific speed-power curve, so the result should not be interpreted as a validated hydrodynamic relationship.

For example, the earlier Port Harcourt–Lagos scenario produced approximately 10.75 knots and 1,496 L under the stated assumptions and ETA constraint.

That means:

> Under the assumptions used by this prototype, approximately 10.75 knots was the lowest feasible speed for the selected ETA.

It does **not** mean that 10.75 knots is the optimum operating speed of a real vessel.

## What this project demonstrates

The main thing I wanted to demonstrate was not a high R² score.

It was the ability to work through a maritime analytics problem:

1. identify a practical operational question;
2. inspect and prepare available data;
3. build a first model;
4. question whether the first validation was appropriate;
5. test generalisation at vessel level;
6. turn predictions into an expected-performance measure;
7. build a simple interface around the result; and
8. identify what would be needed to make the approach useful with real vessel data.

## What is missing compared with a real vessel

The public dataset does not give me the information I would normally want for a serious vessel-performance investigation.

For example, a real implementation could need:

- noon/daily reports;
- AIS position and speed;
- speed through water;
- engine load and RPM;
- fuel consumption by relevant consumer;
- fuel ROB and bunker records;
- draft and trim;
- wind, waves and currents;
- vessel-specific speed/power information;
- hull and propeller condition;
- voyage plan and ETA;
- operational mode and exceptions;
- reliable timestamps and data definitions.

I have **not** tried to invent these fields in this project.

Instead, I documented them as the next data requirements.

## What I learned from looking at real maritime data structures

While working on the project I looked at the Smart Maritime Network Standardised Vessel Dataset (SVD), the IMO Compendium and the Intelligent Ship Transport System voyage-performance-report work.

This was mainly useful for understanding how a real maritime dataset would be structured and why consistent definitions matter.

For example, a production system needs to know whether a distance value is distance through water or over ground, what a fuel value represents, which consumer it belongs to, when the measurement was taken and how the signal is defined.

The current IMO Compendium, approved by FAL 50 in 2026, also includes a dataset for meteorological and oceanographic observations. I found that particularly relevant because the project is moving toward the question of how operating and environmental conditions should be brought together for performance analysis. ([IMO Compendium](https://www.imo.org/en/ourwork/facilitation/pages/imocompendium.aspx), [FAL 50 changes](https://imocompendium.imo.org/public/IMO-Compendium/Current/Changes.pdf))

The project does **not** implement the SVD, IMO Compendium, ISO 19848 or a production VPR system. They are reference points that helped me understand the gap between this public-data exercise and a real vessel-performance application.

## Standards and industry references considered for a real implementation

I have kept a separate note explaining the main standards and industry references I reviewed, including their role in the production-data gap:

- **SVD Version 2.0** — common vessel operational and emissions data definitions.
- **IMO Compendium** — broader maritime data harmonisation and electronic information exchange; the 2026 version adds meteorological and oceanographic observations.
- **ISO 19848:2024** — standard data for shipboard machinery, equipment and operational information.
- **ISO 19847:2024** — shipboard data servers for collecting and sharing field data.
- **ISO 16425:2024** — ship communication-network specifications.
- **ISO 18131:2025** — publish-subscribe ship-shore operational data communication.
- **ISO 28005-1:2024 / ISO 28005-3:2024** — electronic port-clearance data exchange.
- **ISO 19030 Parts 1–3** — measurement of changes in hull and propeller performance.
- **IACS Recommendation 183** — ship data quality.
- **DNV-RP-0497** — data quality assurance.
- **IMO DCS / MARPOL Annex VI** — fuel-consumption data collection and reporting context.
- **DCSA Port Call Standard 2.0** — port-call and just-in-time operational data exchange.
- **Sea Cargo Charter reporting schema** — structured voyage emissions reporting.

These are **references considered**, not standards that this repository claims to implement or certify against.

See [Maritime Standards & Industry References Considered](docs/maritime_standards_and_industry_references.md).

## Important limitations

This project should be read with the following limitations in mind:

- The dataset is public and much simpler than real shipboard data.
- The model does not use live AIS or machinery data.
- The model does not contain a vessel-specific speed-power curve.
- The weather information is a broad category rather than measured environmental data.
- The project does not establish a production-grade fuel-performance baseline.
- The speed-sensitivity calculation is an explicit assumption.
- The model does not account for all of the physical and operational factors that affect fuel consumption.
- There is no genuine time-series backtesting because the dataset does not provide a suitable date/time field.
- The results should not be interpreted as commercial operating recommendations.

## Repository structure

- `data/` — project dataset and maritime data dictionary
- `notebooks/01_eda_and_model_selection.ipynb` — initial EDA and model work
- `notebooks/02_voyage_optimizer.ipynb` — speed/ETA scenario analysis
- `models/` — trained model artifact
- `app/streamlit_app.py` — interactive scenario application
- `retrain_model.py` — model training script
- `scripts/validate_generalisation.py` — vessel-holdout validation
- `scripts/performance_analysis.py` — grouped out-of-fold performance analysis
- `data/maritime_data_dictionary.csv` — current data and production data requirements
- `docs/voyage_performance_analytics.md` — explanation of the performance-analysis extension
- `docs/model_card.md` — model assumptions and limitations
- `docs/svd_production_alignment.md` — production-data thinking and boundary
- `docs/maritime_standards_and_industry_references.md` — standards and industry reference map

## Running locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

To run the vessel-holdout validation:

```bash
python scripts/validate_generalisation.py
```

## Where I would take it next

If I had access to suitable real vessel data, I would not start by making the machine-learning model more complicated.

I would first improve the data and the performance definition:

1. add reliable timestamps and voyage/segment information;
2. bring in AIS and measured weather/ocean data;
3. add draft/trim and engine load/RPM;
4. define fuel measurements and consumers clearly;
5. develop vessel-specific baselines;
6. test time, vessel and route generalisation;
7. investigate data quality and abnormal observations;
8. consider relevant performance measurement methods such as ISO 19030 where the vessel and use case are appropriate;
9. add emissions and cost calculations;
10. only then consider more advanced optimisation or fleet-scale deployment.

That is the main boundary of this project: **the prototype demonstrates the analytical approach; a real system would depend heavily on the quality, history, definitions and context of the underlying vessel data.**

## About

Independent maritime data-science project by Midhun Raj, combining marine engineering and technical-superintendent experience with data analytics, machine learning and maritime digitalisation.

GitHub: https://github.com/midhunrajds
