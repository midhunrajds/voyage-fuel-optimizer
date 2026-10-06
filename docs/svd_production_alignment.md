# Production Data: What Would Be Needed Beyond This POC

## Why this document exists

This project uses a public dataset that is much simpler than the data available in a real vessel-management or performance environment.

I wanted to document that gap rather than imply that the current model is ready for production.

While working through the project, I looked at the Smart Maritime Network Standardised Vessel Dataset (SVD), the IMO Compendium, relevant ISO standards, data-quality guidance and industry reporting/exchange frameworks to understand how real maritime operational data can be described, collected, exchanged and used.

For this project, these references are **production-design references**. They are not implemented or followed as compliance requirements by the POC.

## A simple way to think about a real system

A future vessel-performance workflow could look roughly like:

**ship systems / onboard equipment**

→ data collection and historical storage

→ common definitions, units and data-quality checks

→ AIS + weather/ocean + voyage information

→ voyage/segment performance dataset

→ expected-performance model

→ actual vs expected

→ investigation / alerts / decision support

The exact architecture would depend on the vessel, shipowner, available equipment, data-access arrangements and the intended use case.

I have not built this architecture in the project.

## Current data compared with a real implementation

| Current field | How I use it here | What would be needed in a real system |
|---|---|---|
| ship_id | Identify and group vessels | Stable vessel identity and history |
| ship_type | Basic vessel context | Reliable vessel particulars/classification |
| route_id | Route context | Voyage/route/segment identifiers |
| month | Model feature | Reliable timestamps and reporting periods |
| distance | Model feature | Clearly defined distance, source and unit |
| fuel_type | Model feature | Standard fuel definition and grade/context |
| fuel_consumption | Prediction target | Clearly defined fuel measurement, period and consumer |
| CO2_emissions | Dataset field | Documented emissions calculation and source |
| weather_conditions | Broad weather category | Measured wind, sea state, current and related data |
| engine_efficiency | Dataset-specific feature | Actual machinery measurements such as load/RPM and other relevant signals |

The current fields are enough to demonstrate a modelling workflow. They are not enough to reproduce a full vessel-performance investigation.

## Standards and industry references considered

The following references were reviewed because they address different parts of the production problem. They are a focused list relevant to this POC, not an exhaustive catalogue of maritime standards.

### Data definitions and interoperability

**Smart Maritime Network Standardised Vessel Dataset (SVD) Version 2.0**

Used as a practical reference for common vessel operational and emissions fields, names, units and links to IMO/ISO identifiers.

Reference:
https://smartmaritimenetwork.com/standardised-vessel-dataset-for-noon-reports/

**IMO Compendium on Facilitation and Electronic Business**

The current Compendium approved by FAL 50 in 2026 added a dataset for meteorological and oceanographic observations. This is relevant to the project because environmental context becomes important for performance normalisation and voyage analysis.

Reference:
https://www.imo.org/en/ourwork/facilitation/pages/imocompendium.aspx

Change history:
https://imocompendium.imo.org/public/IMO-Compendium/Current/Changes.pdf

### Onboard machinery and data collection

**ISO 19848:2024 — Standard data for shipboard machinery and equipment**

Relevant to how shipboard sensor and operational data can be named and described consistently.

https://www.iso.org/standard/78262.html

**ISO 19847:2024 — Shipboard data servers for sharing field data at sea**

Relevant to the collection and sharing of shipboard field data.

https://committee.iso.org/standard/78260.html

**ISO 16425:2024 — Ship communication networks**

Relevant to shipboard communication architecture and the environment from which operational data is collected.

https://www.iso.org/standard/78264.html

### Ship-shore and operational exchange

**ISO 18131:2025 — Publish-subscribe architecture on ship-shore data communication**

Relevant to continuous operational-data exchange between ship and shore.

https://www.iso.org/standard/85180.html

**ISO 28005-1:2024 / ISO 28005-3:2024 — Electronic port clearance**

Relevant mainly where a future performance workflow connects with broader ship-shore and port-call processes.

https://www.iso.org/standard/83881.html

https://www.iso.org/standard/83631.html

### Vessel performance

**ISO 19030 Parts 1–3 — Measurement of changes in hull and propeller performance**

Relevant to the idea that vessel performance can be assessed relative to the same vessel over time rather than treating absolute fuel consumption as a complete performance measure.

https://www.iso.org/standard/63774.html

https://www.iso.org/standard/63775.html

https://www.iso.org/standard/63776.html

These standards are not implemented in this POC.

### Data quality

**IACS Recommendation 183 — Ship Data Quality**

Relevant to the reliability and fitness-for-purpose of ship data used in digital applications.

https://iacs.org.uk/resolutions/recommendations/181-200/rec-183-new

**DNV-RP-0497 — Recommended Practice for Data Quality Assurance**

Relevant to the wider management and assurance of data quality.

https://www.dnv.com/digital-trust/recommended-practices/data-quality-assurance-dnv-rp-0497/

### Fuel and emissions

**IMO Data Collection System (DCS)**

Provides the regulatory context for ship fuel-oil consumption data collection and reporting and links fuel data with operational carbon-intensity work.

https://www.imo.org/en/ourwork/environment/pages/data-collection-system.aspx

**Sea Cargo Charter reporting resources**

Includes current reporting resources and a JSON schema for structured voyage-emissions reporting.

https://www.seacargocharter.org/resources/

### Port-call and just-in-time operations

**DCSA Port Call Standard 2.0**

Relevant to a future connection between vessel speed/performance, ETA and port-call planning.

https://dcsa.org/newsroom/port-call-standard-update

## What these references mean for this project

I find it useful to think of the production problem in layers:

**1. Define the data**

SVD / IMO Compendium / ISO 19848

↓

**2. Collect and manage onboard data**

ISO 19847 / ISO 16425

↓

**3. Exchange data between ship and shore**

ISO 18131 and related electronic-exchange standards

↓

**4. Add voyage and port-call context**

VPR concepts / DCSA Port Call / ISO 28005

↓

**5. Define and measure vessel performance**

ISO 19030 and appropriate vessel-specific performance methods

↓

**6. Fuel and emissions reporting**

IMO DCS / Sea Cargo Charter and relevant company/regulatory requirements

↓

**7. Keep the data trustworthy**

IACS Rec. 183 / DNV-RP-0497 and the organisation's own data governance

↓

**8. Apply analytics**

prediction → expected performance → actual vs expected → investigation → decision support

This is a way of thinking about a future production system. It is not the architecture implemented by this repository.

## Examples of important missing information

### Voyage context

A real dataset would benefit from:

- voyage ID;
- segment ID;
- timestamps;
- operational mode;
- ETA;
- voyage plan;
- deviations and exceptions.

### Vessel and operating condition

Useful information could include:

- draft;
- trim;
- displacement/loading condition;
- speed over ground;
- speed through water;
- propeller/engine RPM;
- engine load.

### Environment

Depending on the use case:

- wind;
- waves/sea state;
- current;
- sea temperature;
- other weather/ocean information.

The 2026 IMO Compendium update adding meteorological and oceanographic observations is a useful indication of how environmental information is becoming part of the broader standardised-data picture.

### Fuel

A production dataset would need clearly defined fuel measurements, potentially including:

- fuel used by consumer;
- fuel remaining onboard;
- fuel type/grade;
- bunker records;
- measurement timestamps;
- units and data source.

### Data definitions and quality

A value is much more useful when I know:

- what it means;
- its unit;
- when it was recorded;
- its expected range;
- how it was generated;
- where its definition came from.

The standards and guidance above reinforced a simple point for me: the production problem is not only collecting more data. It is collecting data that remains understandable and trustworthy when it moves between shipboard systems, vendors and shore applications.

## What I actually implemented

The public-data POC currently demonstrates:

- fuel-consumption prediction;
- vessel-aware validation;
- expected-fuel calculation;
- actual-vs-expected screening;
- simple speed/ETA scenario analysis;
- a lightweight data dictionary;
- production-data gap analysis.

It does not demonstrate:

- SVD compliance;
- IMO Compendium implementation;
- ISO 19848/19847 implementation;
- ISO 16425 shipboard networking;
- ISO 18131 ship-shore messaging;
- ISO 19030 performance indicators;
- live DCS exchange;
- DCSA port-call integration;
- production data-quality management;
- real-time cloud ingestion;
- vessel-specific hydrodynamic modelling;
- commercial fuel-saving recommendations.

These are production considerations, not claims about the prototype.

## What I would build next with real data

I would first make the data reliable enough to support a meaningful comparison.

A sensible sequence would be:

1. agree the field definitions and units;
2. establish timestamps and vessel/voyage identity;
3. bring together the available ship, AIS, fuel and environmental data;
4. check missing values, bad readings and other data-quality issues;
5. create voyage/segment records;
6. establish vessel-specific expected performance;
7. validate on future periods and unseen vessels/routes;
8. add exception handling and operational context;
9. consider appropriate performance-measurement methods such as ISO 19030;
10. add emissions/cost calculations;
11. build decision-support features only after the performance signal is trusted.

The important point is that the production challenge is not simply “use a better ML algorithm”. It is **getting reliable, well-defined operational data into a form where the model can be trusted.**
