# Voyage Performance Analytics — Version 2 Design

## Purpose

Version 2 extends the Voyage Fuel Optimizer from a predictive fuel-consumption proof of concept into a voyage performance analytics case study.

The goal is not to imply that the public dataset is a real vessel-performance dataset. Instead, the public data demonstrates the analytical workflow while the repository explicitly maps missing production data.

## Maritime framing

The Smart Maritime Network Standardised Vessel Dataset provides an open reference for common vessel operational and emissions data points. The ISTS voyage-performance report describes voyage performance in terms of voyages, segments, operational modes, events and exceptions. The accompanying data-access guidance highlights the importance of data access, codebooks, normalisation and historical-data storage.

The project therefore separates:

1. Demonstration data — what the current public dataset actually contains.
2. Maritime performance model — concepts required to interpret a voyage operationally.
3. Production data requirements — additional signals required for real deployment.

## Core analytical question

The central question changes from:

How much fuel will this voyage consume?

to:

How does actual fuel consumption compare with expected fuel consumption under comparable operating conditions?

Raw consumption alone does not establish poor performance. Speed, distance, loading condition, weather, sea state, current, machinery condition, operational mode and exceptions can affect expected consumption.

## Performance workflow

Voyage / segment
→ operational and environmental context
→ expected fuel model
→ actual fuel
→ performance deviation
→ operational interpretation

For a production system, the expected-fuel model should be trained and validated against appropriate vessel and voyage data. The current public-data implementation is a portfolio demonstration only.

## Validation

The project keeps the original random row split as a baseline, but adds vessel-grouped validation because repeated observations from the same vessel can make a random split look more generalisable than it really is.

ship_id is used as a grouping variable for validation, not as a predictive feature.

The repository also provides an out-of-fold performance-analysis script. It creates predictions for observations that were not used to train the corresponding model and supports calculation of actual fuel, expected fuel, absolute error and percentage deviation.

No vessel-holdout or out-of-fold metric should be described as production accuracy.

## Voyage segments and exceptions

The ISTS model associates a Voyage Performance Report with a specific segment. The project adopts that conceptual structure without claiming that the public dataset contains true VPR records.

A future production dataset can represent:

- voyage and segment identifiers;
- operational mode;
- start/end timestamps;
- distance and speed;
- ETA;
- cargo/loading context;
- fuel consumers and fuel used;
- fuel ROB;
- weather;
- exceptions such as heavy weather, deviation or technical problems.

These fields allow the performance layer to distinguish normal operation from observations that require contextual interpretation.

## Data standardisation

The project includes data/maritime_data_dictionary.csv as a lightweight portfolio data dictionary.

It distinguishes:

- fields already present in the public demonstration dataset;
- production fields that are currently unavailable;
- maritime concepts associated with the field;
- units and data-source assumptions;
- relevant SVD/ISTS references.

This is intentionally a mapping aid, not a claim that the repository implements the full SVD or IMO Compendium.

## Data architecture

A production architecture would need to preserve data meaning as well as values. The data-access guidance emphasises codebooks describing signals, protocols, formats, units, ranges, precision and intervals. Historical availability should also be explicitly planned rather than assumed.

A practical production pipeline would resemble:

Onboard equipment / ship systems
→ data acquisition and historian
→ codebook / standardisation layer
→ AIS + weather/ocean + voyage plan + fuel records
→ voyage / segment data model
→ data quality and normalisation
→ performance model
→ dashboard / alerts / decision support

## Production gap

The current dataset does not provide enough information to build a validated vessel-specific performance model.

Important missing dimensions include:

- draft and trim;
- engine load and RPM;
- speed through water;
- wind, waves and currents;
- detailed fuel-consumer measurements;
- fuel ROB;
- vessel-specific speed/power relationships;
- voyage segments and operational modes;
- exceptions and deviations;
- high-frequency machinery data;
- robust timestamps and data lineage.

The project treats these as explicit production requirements rather than inventing them.

## Future versions

### Version 2 — Voyage Performance Analytics

- grouped/out-of-fold expected-fuel predictions;
- actual-vs-expected deviation;
- voyage/segment concepts;
- operational modes and exceptions;
- data dictionary;
- production-data gap analysis.

### Version 3 — Voyage Optimisation Decision Support

- vessel-specific speed/power relationships;
- weather and ocean data;
- ETA/fuel/emissions trade-offs;
- route alternatives;
- uncertainty and confidence ranges;
- fleet-level benchmarking.

### Version 4 — Production-oriented architecture

- automated data ingestion;
- data-quality monitoring;
- anomaly detection;
- model monitoring;
- vessel-specific baselines;
- auditable recommendations;
- integration with operational workflows.
