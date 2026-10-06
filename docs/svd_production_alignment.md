# Production Data: What Would Be Needed Beyond This POC

## Why this document exists

This project uses a public dataset that is much simpler than the data available in a real vessel-management or performance environment.

I wanted to document that gap rather than imply that the current model is ready for production.

While working through the project, I looked at the Smart Maritime Network Standardised Vessel Dataset (SVD) and related voyage-performance material to understand how real maritime operational data can be described and organised.

For this project, SVD is a **reference for data definitions and interoperability**. It is not an optimisation algorithm and it is not implemented here.

## A simple way to think about a real system

A production vessel-performance workflow could look roughly like:

**ship systems / onboard equipment**

→ data collection and historical storage

→ common definitions, units and data quality checks

→ AIS + weather/ocean + voyage information

→ voyage/segment performance dataset

→ expected-performance model

→ actual vs expected

→ investigation / alerts / decision support

The exact architecture would depend on the vessel, shipowner, available equipment, data-access arrangements and the intended use case.

I have not built this architecture in the project.

## What the current dataset gives me

| Current field | How I use it here | What would be needed in a real system |
|---|---|---|
| `ship_id` | Identify and group vessels | Stable vessel identity and history |
| `ship_type` | Basic vessel context | Reliable vessel particulars/classification |
| `route_id` | Route context | Voyage/route/segment identifiers |
| `month` | Model feature | Reliable timestamps and reporting periods |
| `distance` | Model feature | Clearly defined distance, source and unit |
| `fuel_type` | Model feature | Standard fuel definition and grade/context |
| `fuel_consumption` | Prediction target | Clearly defined fuel measurement, period and consumer |
| `CO2_emissions` | Dataset field | Documented emissions calculation and source |
| `weather_conditions` | Broad weather category | Measured wind, sea state, current and related data |
| `engine_efficiency` | Dataset-specific feature | Actual machinery measurements such as load/RPM and other relevant signals |

The current fields are enough to demonstrate a modelling workflow. They are not enough to reproduce a full vessel-performance investigation.

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

### Fuel

A production dataset would need clearly defined fuel measurements, potentially including:

- fuel used by consumer;
- fuel remaining onboard;
- fuel type/grade;
- bunker records;
- measurement timestamps;
- units and data source.

### Data definitions

This is easy to overlook.

A value is much more useful when I know what it means, its unit, when it was recorded, its expected range and how it was generated.

The maritime data standards I reviewed reinforced this point. The production problem is not only collecting more data; it is making sure that data from different sources can be understood consistently.

## SVD and voyage-performance reports

I looked at two related ideas while developing the project.

**SVD:** useful as a reference for standardised vessel operational and emissions data points.

**Voyage Performance Report / noon-report concepts:** useful for thinking about voyage segments, operational modes, events and exceptions.

I treat them as complementary ideas:

**data definitions → operational context → analytics**

The project does not implement either system in full.

In particular, this repository does not claim to provide:

- full SVD compliance;
- IMO Compendium implementation;
- ISO 19848 data exchange;
- real noon-report ingestion;
- a production VPR system.

## What I would build next with real data

I would first make the data reliable enough to support a meaningful comparison.

A sensible sequence would be:

1. agree the field definitions and units;
2. establish timestamps and vessel/voyage identity;
3. bring together the available ship, AIS, fuel and environmental data;
4. check missing values, outliers and obvious bad readings;
5. create voyage/segment records;
6. establish vessel-specific expected performance;
7. validate on future periods and unseen vessels/routes;
8. add exception handling and operational context;
9. add emissions/cost calculations;
10. build decision-support features only after the performance signal is trusted.

The important point is that the production challenge is not simply “use a better ML algorithm”. It is **getting reliable, well-defined operational data into a form where the model can be trusted.**

## Boundary of this POC

The current project demonstrates:

- fuel-consumption prediction;
- vessel-aware validation;
- expected-fuel calculation;
- actual-vs-expected screening;
- simple speed/ETA scenario analysis;
- awareness of the production data requirements.

It does not demonstrate:

- live vessel data ingestion;
- large-scale streaming;
- cloud production architecture;
- real-time fleet monitoring;
- vessel-specific hydrodynamic modelling;
- commercial fuel-saving recommendations.

Those are the next layers of a real system, not claims about this project.
