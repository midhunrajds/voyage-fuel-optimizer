# Voyage Performance Analytics — Version 2

## Why I extended the project

The first version of the project answered a straightforward prediction question:

> How much fuel does the model expect for a voyage record?

I wanted to take the project one step further and make the result closer to something a vessel-performance analyst could actually investigate.

That led to a second question:

> How does actual fuel consumption compare with what the model expected?

This is the main idea behind Version 2.

It is still a public-data portfolio project. The purpose is to demonstrate the approach, not to claim that the public dataset represents a real shipboard performance system.

## The basic idea

**actual fuel → expected fuel → deviation → investigation**

The expected value comes from grouped out-of-fold predictions.

If:

actual fuel > expected fuel

the observation has a positive fuel deviation.

That is a reason to look at the observation more closely. It is not, by itself, a diagnosis.

For example, a real investigation might ask:

- Was the vessel operating at a different speed?
- Was the draft or trim different?
- Was there heavy weather or adverse current?
- Was the vessel in a different operating mode?
- Was there a machinery or hull condition issue?
- Was the fuel measurement itself reliable?
- Was there an operational exception or voyage deviation?

The current dataset cannot answer most of those questions. That is one of the main findings of the project.

## Why I used vessel-grouped validation

The dataset contains repeated observations from the same vessels.

A normal random row split can therefore be misleading. An observation from Vessel A may be in the test set while other observations from Vessel A are in the training set.

For this reason I added:

- 5-fold GroupKFold using ship_id;
- a separate test where 24 complete vessels were kept out of training.

The model is still the same basic Random Forest approach. The change is mainly about asking a better validation question.

## Current results

### Grouped out-of-fold analysis

1,440 records are assigned an out-of-fold expected-fuel value.

| Metric | Result |
|---|---:|
| MAE | 610.52 L |
| RMSE | 1,071.39 L |
| R² | 0.9520 |
| Mean deviation | -5.59 L |
| Median deviation | 10.35 L |
| Mean absolute deviation | 610.52 L |

### Held-out vessels

The separate test trains on 96 vessels and evaluates on 24 unseen vessels.

| Metric | Result |
|---|---:|
| MAE | 790.97 L |
| RMSE | 1,330.34 L |
| R² | 0.9470 |

The result is useful evidence from this dataset, but it is not a production accuracy claim.

## What the project currently produces

The performance workflow produces:

- actual fuel;
- expected fuel;
- absolute error;
- fuel deviation;
- percentage fuel deviation;
- vessel-level summaries.

The Streamlit application provides an interactive view of the scenario and performance calculations.

The GitHub Actions workflow runs the analysis scripts and stores the generated out-of-fold results as an artifact.

## Thinking about a real voyage

In real vessel-performance work, a voyage is not just one number for distance and one number for fuel.

Performance depends on what part of the voyage is being considered and what the vessel was doing during that period.

I looked at the Intelligent Ship Transport System voyage-performance-report material to understand this idea. It uses voyage segments, operational modes and exceptions to give performance observations context.

I use those concepts here only as a way to think about the next stage of the project.

The public dataset does **not** contain true VPR records or a full voyage/segment model.

A future real-data version could include:

- voyage ID;
- segment ID;
- start/end time;
- operational mode;
- distance;
- speed;
- ETA;
- fuel used;
- fuel remaining onboard;
- weather and sea state;
- deviations or exceptions.

That would make an actual-vs-expected result much easier to interpret.

## Standards and industry references I reviewed

Because the project uses a simplified public dataset, I wanted to understand what would normally sit around the analytics in a real implementation.

The main references I reviewed were:

### SVD Version 2.0

The Smart Maritime Network Standardised Vessel Dataset provides a common reference for vessel operational and emissions data, including standard data-point names, units, IMO Data Numbers and ISO 19848 Universal IDs.

I used it mainly to identify the type of operational fields and definitions that are missing from the public dataset.

Reference:
https://smartmaritimenetwork.com/standardised-vessel-dataset-for-noon-reports/

### IMO Compendium

The IMO Compendium is a broader reference for harmonised maritime electronic data exchange. The version approved by FAL 50 in 2026 added a dataset for meteorological and oceanographic observations.

That is particularly relevant to the direction of this project because measured environmental context becomes important when moving from simple fuel prediction to performance analysis and voyage optimisation.

Reference:
https://www.imo.org/en/ourwork/facilitation/pages/imocompendium.aspx

### ISO 19848:2024 and ISO 19847:2024

ISO 19848 covers standard data for shipboard machinery, equipment and operational information. ISO 19847 covers shipboard data servers used to collect and share field data.

For this project, these standards helped me frame the gap between a simple field such as engine_efficiency and the actual machinery data I would expect in a real system.

References:
https://www.iso.org/standard/78262.html
https://committee.iso.org/standard/78260.html

### ISO 19030

The ISO 19030 series provides methods and indicators for measuring changes in hull and propeller performance over time.

This is useful conceptually because a real performance analysis should distinguish between absolute fuel consumption and a vessel's performance relative to an appropriate baseline and operating condition.

References:
https://www.iso.org/standard/63774.html
https://www.iso.org/standard/63775.html
https://www.iso.org/standard/63776.html

### Data quality

IACS Recommendation 183 addresses ship data quality, while DNV-RP-0497 provides a framework for data-quality assurance.

These references reinforce an important lesson from this project: better analytics depends on reliable and well-defined data, not only on a more complicated model.

References:
https://iacs.org.uk/resolutions/recommendations/181-200/rec-183-new
https://www.dnv.com/digital-trust/recommended-practices/data-quality-assurance-dnv-rp-0497/

### Ship-shore and port-call data exchange

ISO 18131:2025 covers publish-subscribe ship-shore operational-data communication.

DCSA Port Call Standard 2.0 provides a current industry approach to standardised operational information exchange around port calls and Just-in-Time operations.

These are not implemented in this POC. They are relevant when considering how a future performance system could connect to operational data beyond a static dataset.

References:
https://www.iso.org/standard/85180.html
https://dcsa.org/newsroom/port-call-standard-update

### Fuel and emissions reporting

The IMO Data Collection System provides the regulatory context for ship fuel-oil consumption reporting.

The Sea Cargo Charter also maintains structured reporting resources, including a JSON schema.

These are useful background for thinking about consistent fuel and emissions data, but they are not implemented by this project.

References:
https://www.imo.org/en/ourwork/environment/pages/data-collection-system.aspx
https://www.seacargocharter.org/resources/

A fuller list is maintained in [Maritime Standards & Industry References Considered](maritime_standards_and_industry_references.md).

## Data standardisation

The project includes a lightweight data dictionary separating the fields available in the public dataset from fields I would want in a production implementation.

The main lesson was simple: a value is not enough. I need to know what it means, its unit, when it was recorded, what period it covers and, where relevant, which vessel, voyage segment or consumer it belongs to.

This project does **not** implement the SVD, IMO Compendium, ISO standards or the related reporting/exchange systems.

## What is missing

The main gaps are practical data gaps rather than missing machine-learning algorithms.

Examples include:

- reliable timestamps;
- AIS;
- speed through water;
- draft and trim;
- engine load and RPM;
- measured wind, waves and current;
- fuel consumption by relevant consumer;
- fuel ROB;
- vessel-specific speed/power information;
- voyage segments and operational modes;
- technical or operational exceptions;
- historical data with enough consistency to establish a vessel baseline.

Without these, it would be difficult to turn a positive fuel deviation into a reliable operational conclusion.

## What I would do with real data

I would take the following order rather than immediately choosing a more complicated ML model:

1. establish the data definitions and timestamps;
2. build a reliable voyage/segment dataset;
3. check data quality and missing values;
4. align AIS, machinery, fuel and environmental data;
5. establish vessel-specific expected-performance baselines;
6. test the model on future periods and unseen vessels/routes;
7. investigate abnormal deviations with operational context;
8. consider established performance measurement methods where appropriate, such as ISO 19030;
9. add emissions and cost;
10. build the recommendation layer only after the underlying performance signal is reliable.

That is the intended direction of this portfolio project.

## Boundary of Version 2

Version 2 demonstrates:

- vessel-grouped validation;
- out-of-fold expected fuel;
- actual-vs-expected comparison;
- simple performance screening;
- production-data gap analysis.

It does not demonstrate:

- a real vessel-performance baseline;
- real-time data ingestion;
- vessel-specific hydrodynamic modelling;
- validated commercial fuel savings;
- automated operational recommendations;
- compliance or certification against the referenced standards.

The distinction is deliberate.

## Next step

The next portfolio project moves to a different data problem: AIS movement combined with environmental data.

That project will look at vessel behaviour under different traffic and environmental conditions rather than repeating the same fuel-prediction exercise.
