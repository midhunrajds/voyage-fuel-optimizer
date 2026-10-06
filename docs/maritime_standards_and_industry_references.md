# Maritime Standards & Industry References Considered

## Why this exists

This project is a public-data proof of concept. I do not have access to live shipboard sensor feeds, proprietary noon reports, fleet historians, commercial weather services or the data pipelines used by ship managers and maritime software providers.

Rather than pretending those capabilities are present, I used publicly available data and documented what I would need to consider for a real implementation.

This note records the main standards, data models and industry references I reviewed while thinking about that production gap.

**Important:** These references informed the design and the way I describe the production-data requirements. The project does **not** claim compliance with, or implementation of, all of these standards.

This is a focused list relevant to vessel performance, operational data, ship-to-shore exchange and fuel/emissions analysis. It is not intended to be an exhaustive list of maritime standards.

## 1. Vessel operational data and meaning

### Smart Maritime Network — Standardised Vessel Dataset (SVD) Version 2.0

The SVD is the closest match to the data problem in this project. The current SMN page describes SVD Version 2.0 as an open reference for common vessel operational and emissions data, including standard data-point names, units, IMO Data Numbers and ISO 19848 Universal IDs.

I used it mainly to think about what a production vessel-performance dataset would need to define consistently: vessel identity, voyage information, speed, distance, fuel, weather, emissions and related operational fields.

The repository does **not** implement the SVD.

Reference: https://smartmaritimenetwork.com/standardised-vessel-dataset-for-noon-reports/

Version 2.0 announcement: https://smartmaritimenetwork.com/2025/05/28/smart-maritime-council-adds-emissions-data-to-standardised-vessel-dataset-with-version-2-0-update/

Open-source implementation: https://github.com/WMS-Ceataec/standardised-vessel-dataset

### IMO Compendium on Facilitation and Electronic Business

The IMO Compendium is the wider maritime reference model for standardised electronic data exchange.

The current version approved by FAL 50 in 2026 added a dataset for meteorological and oceanographic observations. That is particularly relevant to the direction of this project because environmental data becomes increasingly important when moving from simple fuel prediction toward vessel-performance analysis and voyage optimisation.

Reference: https://www.imo.org/en/ourwork/facilitation/pages/imocompendium.aspx

Current change history: https://imocompendium.imo.org/public/IMO-Compendium/Current/Changes.pdf

## 2. Shipboard machinery and operational data

### ISO 19848:2024

ISO 19848:2024 covers standard data for shipboard machinery and equipment and provides requirements/guidance for capturing and processing data from sensors and ship operational information.

This is relevant to the gap between the project's simple engine_efficiency field and the machinery data I would want in a real system.

A production model could require clearly identified and defined measurements such as engine load, RPM and other machinery signals rather than a generic efficiency value.

Reference: https://www.iso.org/standard/78262.html

### ISO 19847:2024

ISO 19847:2024 covers shipboard data servers used to collect data from shipboard machinery and systems and share that data safely and efficiently. It references the data structure of ISO 19848.

For this project, this is part of the conceptual path from onboard measurements to a dataset that can eventually be used ashore.

Reference: https://committee.iso.org/standard/78260.html

### ISO 16425:2024

ISO 16425:2024 covers the installation of ship communication networks for shipboard equipment and systems, including network architecture, operation, testing and cybersecurity considerations.

I include it here because a real analytics system ultimately depends on the shipboard environment from which operational data originates.

This project does not implement shipboard networking.

Reference: https://www.iso.org/standard/78264.html

## 3. Ship-to-shore data exchange

### ISO 18131:2025

ISO 18131:2025 specifies general requirements for publish-subscribe architecture for ship-shore operational data communication. It covers concepts including brokers, publishers, subscribers, cloud-based data management, security and data models.

This is relevant when thinking beyond a static CSV toward continuous operational data exchange.

The project does not implement this architecture; it is a production consideration.

Reference: https://www.iso.org/standard/85180.html

### ISO 28005-1:2024 / ISO 28005-3:2024

The ISO 28005 series covers electronic port-clearance information exchange.

For this project, these standards are adjacent rather than central. They become more relevant if the performance workflow is eventually connected with port-call and ship-shore operational processes.

References: https://www.iso.org/standard/83881.html and https://www.iso.org/standard/83631.html

## 4. Vessel performance

### ISO 19030 series

ISO 19030 provides methods and performance indicators for measuring changes in hull and propeller performance over time.

This is particularly important conceptually.

A vessel-performance system should not simply label a high fuel number as bad performance. A more meaningful question can be whether the same vessel's performance has changed relative to a suitable baseline and comparable operating conditions.

The current ISO pages show Parts 1–3 as current after review/confirmation in 2022.

References:

- Part 1 — General principles: https://www.iso.org/standard/63774.html
- Part 2 — Default method: https://www.iso.org/standard/63775.html
- Part 3 — Alternative methods: https://www.iso.org/standard/63776.html

I have not implemented ISO 19030 in this POC.

## 5. Data quality

### IACS Recommendation 183 — Ship Data Quality

IACS Recommendation 183 addresses ship data quality.

This supports an important lesson from the project: before trusting a performance model, the underlying operational data needs to be reliable and fit for its intended use.

Reference: https://iacs.org.uk/resolutions/recommendations/181-200/rec-183-new

### DNV-RP-0497 — Recommended Practice for Data Quality Assurance

DNV-RP-0497 provides a structured approach to assessing and improving data quality and data-quality management.

I use this as a reference for the idea that data quality is not just a cleaning step in Python; it is part of the wider management of operational data.

Reference: https://www.dnv.com/digital-trust/recommended-practices/data-quality-assurance-dnv-rp-0497/

## 6. Fuel and emissions reporting context

### IMO Data Collection System (DCS)

The IMO DCS requires ships of 5,000 GT and above to collect and report fuel-oil consumption data, and IMO uses the resulting data in its work on operational carbon intensity.

This is relevant background for understanding why fuel data in a production maritime analytics system needs clear definitions, reporting periods and verification.

Reference: https://www.imo.org/en/ourwork/environment/pages/data-collection-system.aspx

### Sea Cargo Charter digital reporting resources

The Sea Cargo Charter currently publishes a reporting template, 2026 reporting changes and a JSON schema.

This is not a vessel-performance standard, but it is a useful example of the wider move toward structured, machine-readable voyage emissions reporting.

Reference: https://www.seacargocharter.org/resources/

## 7. Port-call and voyage planning context

### DCSA Port Call Standard 2.0

DCSA published Port Call Standard 2.0 in December 2025. It updates the Just-in-Time/port-call data exchange approach and provides a more practical operational information structure for organisations involved in port-call planning.

This becomes relevant when a fuel/performance model is connected to ETA, port calls and just-in-time arrival decisions.

Reference: https://dcsa.org/newsroom/port-call-standard-update

## 8. How these references relate to this project

I find it useful to think of the production problem in layers:

**Data meaning**  
SVD / IMO Compendium / ISO 19848

↓

**Onboard collection and shipboard systems**  
ISO 19847 / ISO 16425

↓

**Ship-to-shore exchange**  
ISO 18131 and related electronic-exchange standards

↓

**Voyage and port-call context**  
VPR concepts / DCSA Port Call / ISO 28005

↓

**Performance measurement**  
ISO 19030 and vessel-specific performance methods

↓

**Fuel and emissions reporting**  
IMO DCS / Sea Cargo Charter and related reporting frameworks

↓

**Data quality and governance**  
IACS Rec. 183 / DNV-RP-0497 and the relevant company/data governance rules

↓

**Analytics**  
prediction → expected performance → actual vs expected → investigation → decision support

This is a way of thinking about a future production system. It is not the architecture implemented by this repository.

## 9. What I actually implemented

The public-data POC currently demonstrates:

- fuel-consumption prediction;
- vessel-grouped validation;
- held-out-vessel testing;
- out-of-fold expected-fuel values;
- actual-vs-expected fuel deviation;
- a simple speed/ETA scenario;
- a lightweight maritime data dictionary;
- documentation of production data requirements.

The repository does **not** implement:

- SVD compliance;
- IMO Compendium implementation;
- ISO 19848/19847 implementation;
- ISO 18131 ship-shore messaging;
- ISO 19030 performance indicators;
- live DCS data exchange;
- DCSA port-call integration;
- production data-quality management;
- real-time cloud ingestion;
- commercial voyage optimisation.

## 10. Why I included these references

The purpose is not to make the project look more sophisticated.

It is the opposite.

The more I looked into real maritime data, the clearer the limitations of the public dataset became.

That helped me draw a line between:

**what I can demonstrate with public data**

and

**what would have to be built, verified and governed before a similar idea could be trusted in a real vessel-performance environment.**

That boundary is intentional.