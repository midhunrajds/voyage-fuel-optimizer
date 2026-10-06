# SVD-Aligned Production Data Architecture

The project does not implement the complete SVD, IMO Compendium, ISO 19848 model, or a production VPR system. This document makes the production-data path explicit.

## Why SVD matters

The Smart Maritime Network SVD is a free, vendor-neutral reference for common vessel operational and emissions data points, including standard names, units, IMO Data Numbers and ISO 19848 Universal IDs. Version 2.0 also extends the model into emissions reporting.

For this portfolio project, SVD is treated as a **data vocabulary and interoperability reference**, not as an analytics algorithm.

## Production data flow

Onboard equipment / ship systems → data acquisition & historian → codebook / standardisation layer → SVD-aligned operational dataset → AIS + weather/ocean + voyage-plan context → voyage / segment model → data-quality & normalisation → expected-performance model → actual-vs-expected analysis → exceptions / alerts / decision support.

The standardisation layer should preserve source meaning while associating each field with a stable definition, unit, timestamp and lineage.

## POC-to-production mapping

| Current POC field | Maritime concept | Production interpretation |
|---|---|---|
| ship_id | Vessel identity | Stable vessel key for grouping, benchmarking and validation |
| ship_type | Vessel type | Vessel classification/context |
| route_id | Voyage/route context | Route or voyage reference |
| distance | Distance sailed | Documented definition and unit required |
| fuel_type | Fuel information | Fuel category/grade context |
| fuel_consumption | Fuel consumed | Defined period, consumer and unit required |
| CO2_emissions | Emissions | Reporting methodology must be retained |
| weather_conditions | Weather | Public category; production should use measurable observations |
| engine_efficiency | Machinery proxy | Demo proxy; production should use documented telemetry |

## Production dimensions to add

Important missing dimensions are voyage and segment identifiers; operational mode and exception/deviation context; ETA and timestamps; speed over ground and speed through water; draft and trim; engine load and RPM; wind, sea state and current; fuel remaining onboard and fuel used by consumer; and codebook/data-definition references.

These matter because expected fuel depends on operating context. A high deviation cannot be interpreted correctly without knowing whether the vessel was in heavy weather, at a different draft/trim, following a different speed profile, or affected by an operational or technical exception.

## SVD and VPR are complementary

**SVD → what the data point means**

**VPR → where the data point sits in voyage/performance context**

**Analytics → what we do with the standardised data**

This distinction prevents the project from implying that a data standard itself performs fuel optimisation.

## Current boundary

The POC demonstrates predictive fuel modelling, vessel-grouped validation, out-of-fold expected-fuel estimates, actual-vs-expected deviation, scenario-based speed/ETA analysis, and production-data gap analysis.

It does not demonstrate validated vessel-specific speed-power curves, real noon-report ingestion, real-time AIS/weather ingestion, SVD XML/JSON interchange, production data-quality monitoring, or production fleet recommendations.

## Portfolio positioning

> A maritime analytics proof of concept that takes public voyage data from predictive modelling through expected-performance analysis and scenario decision support, while explicitly designing the data requirements and standardisation path needed for a production vessel-performance system.
