**NEWTON SCHOOL OF TECHNOLOGY**

Data Visualisation & Analytics — Capstone 2

**India Air Quality Intelligence System**

A Deep Exploratory Analysis of PM2.5 Pollution Patterns, Drivers, and Forecasting (2022–2025)

| Sector | Environmental Analytics / Public Health |
| :---- | :---- |
| **Team ID** | Group No. 16 |
| **Team Members** | Yashi Agarwal, Vani Rudra, Satya Yadav, Rohit Kumar, Mohan Kumar CR, Aryan Vibhuti |
| **Institute** | Newton School of Technology |
| **GitHub Repository** | [Github Link](https://github.com/3ncryptor/DVA_Capstone_2) |
| **Tableau Dashboard** | [Tableau Dashboard Link](https://public.tableau.com/app/profile/yashi.agarwal1143/viz/Air_Quality_Final_Workbook11_17774593482750/Dashboard1) |
| **Submission Date** | April 29, 2026 |

**2\.  Executive Summary**

Air pollution is one of India's most urgent and measurable public health challenges. This project analysed hourly PM2.5 readings across 29 Indian cities spanning 2022 to 2025, combining a rigorous Python-based analytical pipeline with an interactive Tableau dashboard to surface the patterns, causes, and concentrations of dangerous pollution.

## **The problem**

India consistently records some of the world's highest ambient PM2.5 concentrations. With a national average of 34.74 µg/m³ — more than double the WHO safe limit of 15 µg/m³ — and peak readings reaching 581.1 µg/m³, the air quality crisis imposes a severe and avoidable burden on public health, productivity, and quality of life. Policy-makers and city administrators lack a consolidated, evidence-based picture of when, where, and why pollution peaks occur.

## **The approach**

Raw hourly sensor data was ingested, validated, cleaned, and enriched through a fully automated Python pipeline. Feature engineering created lag variables, rolling averages, seasonal flags, and meteorological interaction indicators. A Random Forest forecasting model was trained on a time-ordered holdout to provide short-horizon PM2.5 predictions. All findings were then visualised in a six-page Tableau dashboard.

## **Key findings**

* Pollution is structurally concentrated: Gurugram (78.71 µg/m³) and Delhi (56.29 µg/m³) are chronic outliers — not occasional spikes — demanding priority structural intervention.

* Winter is the crisis season: nearly all 740 recorded extreme pollution events cluster in November through January, driven by meteorological stagnation, crop residue burning, and festival activity.

* Low wind combined with high humidity is the highest-risk meteorological state, producing severe pollution probability nearly double that of all other weather combinations.

* Festivals and crop burning amplify baseline pollution by 15–20%, with an average impact spread of 28.89 µg/m³ above non-event conditions.

## **Key recommendations**

* Deploy a winter emergency protocol in Gurugram, Delhi, Kolkata, and Patna each year from October onwards, including vehicle and industrial restrictions triggered by forecasted meteorological thresholds.

* Enforce and extend the stubble-burning ban across post-monsoon agricultural zones, with satellite monitoring and rapid-response teams active from September.

* Invest in real-time early-warning infrastructure using the forecasting model developed in this project to issue public health advisories 6–24 hours ahead of dangerous spikes.

**3\.  Sector & Business Context**

## **Sector overview**

This project operates at the intersection of environmental analytics and public health policy. India's Central Pollution Control Board (CPCB) and State Pollution Control Boards monitor ambient air quality through a national network of continuous ambient air quality monitoring stations (CAAQMS). Despite this infrastructure, actionable, city-specific, and event-aware intelligence remains underdeveloped.

PM2.5 — particulate matter smaller than 2.5 micrometres — is the most clinically significant air pollutant because it penetrates deep into lung tissue and enters the bloodstream. The World Health Organisation's annual mean guideline is 5 µg/m³; India's national standard is 40 µg/m³. India's average across this dataset is 34.74 µg/m³, and individual city peaks reach 78.71 µg/m³ on an annual average basis, with hourly spikes as high as 581.1 µg/m³.

## **The decision-maker this project serves**

The primary audience is city-level environmental policy administrators, municipal commissioners, and state environment department heads who must allocate enforcement resources, design seasonal restrictions, and communicate public health advisories. A secondary audience includes national-level planners at CPCB and the Ministry of Environment, Forest and Climate Change.

## **Why this problem was chosen**

Air pollution in India is frequently discussed but rarely analysed in a structured, reproducible, city-specific manner that separates seasonal baselines from event-driven spikes and meteorological amplification. Most public discourse relies on annual averages that obscure the extreme concentration and short-duration nature of the worst events. This project addresses that gap by building an hourly-resolution, multi-city analytical system with a forecasting capability.

## **Business value of solving it**

Quantifying the who, when, and why of pollution peaks enables targeted policy over blanket restrictions, reducing both compliance costs for businesses and exposure costs for residents. Even a 10% reduction in severe pollution days in the four critical-quadrant cities would represent a measurable public health gain worth billions of rupees in avoided healthcare expenditure and productivity loss.

**4\.  Problem Statement & Objectives**

## **Formal problem definition**

| India's air quality crisis is not uniform — it is a structured, state-dependent phenomenon driven by seasonal cycles, amplified by meteorological stagnation, and intensified by episodic events including crop burning and festivals. The central question is: can we use historical hourly sensor data to reliably identify the temporal patterns, spatial inequalities, meteorological dependencies, event-driven amplifications, and extreme-event dynamics that govern PM2.5 concentrations across Indian cities — and can we use those findings to predict future pollution levels with enough lead time for policy action? |
| :---- |

## **Project scope**

**In scope:**

* 29 Indian cities; hourly PM2.5 readings from 2022 to 2025

* Full EDA pipeline: temporal, spatial, meteorological, and event-based analysis

* Short-horizon PM2.5 forecasting for individual cities at 1h, 6h, 12h, 24h, and 48h horizons

* A six-page interactive Tableau dashboard for operational use

**Out of scope:**

* Real-time data ingestion or live API connections

* Health outcome modelling (e.g., hospital admission forecasting)

* Pollutant species other than PM2.5 (NO2, SO2, O3 are not modelled)

## **Success criteria**

* All six EDA analysis modules produce valid, non-empty output CSVs for the full national dataset

* The Random Forest model achieves R² \> 0.40 on the time-ordered test set for the 1-hour forecast horizon

* The Tableau dashboard is publicly accessible with City, Season, and Year filters operating across all six pages

* The report meets the 10–15 page requirement with all 18 outline sections completed

**5\.  Data Description**

## **Dataset source**

**Dataset: INDIA\_AQI\_COMPLETE\_20251126.csv**

Source: Compiled air quality sensor network data covering continuous ambient monitoring stations across 29 Indian cities, spanning August 2022 to November 2025\. The dataset was assembled and curated for this capstone project and is stored in the repository at data/raw/ (tracked via Git LFS).

| 29 Cities | 2022–2025 Time Period | Hourly Granularity | 800,000+ Approx. Rows |
| :---: | :---: | :---: | :---: |

## **Key columns**

| Column | Type | Description |
| :---- | :---- | :---- |
| **Datetime** | DateTime | Hourly timestamp for the observation |
| **City** | String | Name of the Indian city (29 unique values) |
| **PM2\_5\_ugm3** | Float | PM2.5 concentration in micrograms per cubic metre — the primary target variable |
| **Humidity\_Percent** | Float | Ambient relative humidity (0–100%) |
| **Wind\_Speed\_10m\_kmh** | Float | Wind speed at 10m height in km/h |
| **Temp\_2m\_C** | Float | Air temperature at 2m height in degrees Celsius |
| **Season** | String | Derived season label: Winter, Summer, Monsoon, Post-Monsoon |
| **Festival\_Period** | Integer | Binary flag: 1 if the date falls within a recognised festival period |
| **Crop\_Burning\_Season** | Integer | Binary flag: 1 if the date falls within the agricultural burning season |
| **Latitude / Longitude** | Float | City geographic coordinates for map visualisations |

## **Data limitations and known biases**

* Urban sensor bias: all 29 cities are state capitals or major urban centres; rural and peri-urban populations are not represented.

* Sensor downtime: missing periods exist for several cities during maintenance windows, particularly affecting monsoon months.

* Festival and crop-burning flags are calendar-derived binary indicators, not measured emission event flags — they are a proxy, not a direct emission measurement.

* The national average of 34.74 µg/m³ understates true exposure for the most polluted cities, since the distribution is heavily right-skewed.

**6\.  Data Cleaning & ETL Pipeline**

All cleaning and transformation steps were executed in Python. The pipeline is fully automated and reproducible — running python cli.py \--stage profiling re-executes every step from raw CSV to analytical output. The key modules are src/preprocessing/validation.py, cleaning.py, and feature\_engineering.py.

## **Validation**

* Schema check: confirmed presence of all required columns (Datetime, City, PM2\_5\_ugm3, Humidity\_Percent, Wind\_Speed\_10m\_kmh).

* Range validation: flagged and logged counts of negative PM2.5 readings, humidity values outside 0–100%, and negative wind speeds.

* Duplicate detection: counted and logged exact duplicate rows across all columns.

## **Cleaning steps**

* Duplicate removal: all exact duplicate rows dropped.

* Negative PM2.5: rows with PM2\_5\_ugm3 \< 0 removed entirely (sensor malfunction indicator).

* Humidity clipping: values outside 0–100% clipped to the valid range rather than dropped, preserving temporal continuity.

* Wind speed correction: negative wind speed values converted to their absolute value (sign error in sensor data, not true negative wind).

* Sorting: data sorted by City, then Datetime to ensure time-series continuity before lag and rolling feature computation.

## 

## **Feature engineering — new columns created**

| Feature | Method | Purpose |
| :---- | :---- | :---- |
| **pm25\_lag\_1 / \_24 / \_168** | Per-city shift(1), shift(24), shift(168) | Capture 1-hour, 24-hour, and 7-day autocorrelation in PM2.5 |
| **pm25\_roll\_24, pm25\_roll\_std\_24** | 24-hour rolling mean and std | Smooth signal and measure local volatility |
| **pm25\_deviation** | PM2.5 minus rolling mean | Isolate event-driven spikes from seasonal baseline |
| **year, month, hour, day\_of\_week** | Extracted from Datetime | Enable temporal segmentation in analysis and forecasting |
| **pm25\_category** | Threshold classification | Indian AQI categories: Good to Severe |
| **is\_severe** | Boolean: PM2.5 \> 250 | Target variable for extreme event analysis |
| **low\_wind** | Boolean: wind speed \< 5 km/h | Meteorological stagnation flag for interaction analysis |
| **high\_humidity** | Boolean: humidity \> 70% | Humidity accumulation flag for fog/haze conditions |
| **is\_festival, is\_crop\_burning** | Cast from integer flags | Event-period indicators for amplification analysis |

Key assumption: Negative wind speed readings were treated as sign-entry errors and corrected via absolute value rather than dropped, on the basis that the magnitude carries valid meteorological information. Rows with humidity slightly outside the sensor range were clipped rather than removed to preserve temporal continuity in city-level time series.

**7\.  KPI & Metric Framework**

The following KPIs were defined to operationalise the project's analytical objectives. Each is directly computable from the cleaned, engineered dataset and is surfaced in the Tableau dashboard.

| KPI | Definition / Formula | Why it matters | Maps to objective |
| :---- | :---- | :---- | :---- |
| **National Avg PM2.5** | Mean of PM2\_5\_ugm3 across all cities and time | Establishes baseline exposure level; benchmark for city comparison | Spatial inequality (P2) |
| **% Severe Days** | Proportion of hourly rows where PM2.5 \> 250 µg/m³ | Captures tail risk; directly relevant to health emergency planning | Tail risk (P2, P6) |
| **City Avg PM2.5** | Per-city mean of PM2\_5\_ugm3 | Identifies chronic outlier cities requiring priority intervention | City archetypes (P3) |
| **Coefficient of Variation (CV)** | Std / Mean per city | Separates stable-high from volatile cities; guides different policy responses | City archetypes (P3) |
| **Event Delta** | PM2.5 minus 24h rolling baseline during event periods | Isolates event-driven amplification from background pollution | Event amplification (P5) |
| **Severe Probability** | Mean of is\_severe flag by weather/season group | Identifies highest-risk meteorological conditions | Meteorological dependencies (P4) |
| **Extreme Event Count** | Count of rows where PM2.5 \> 250, by city and season | Quantifies where and when extreme events concentrate | Extreme dynamics (P6) |
| **Forecast MAE / R²** | Test-set mean absolute error and coefficient of determination per horizon | Measures predictive utility for early-warning use case | Forecasting (P8) |

**8\.  Exploratory Data Analysis**

## **Overview — national picture**

| 34.74 µg/m³ National avg PM2.5 | 581.1 µg/m³ Maximum PM2.5 | 23.39 µg/m³ Std deviation | 19.44% % Severe Days | 7 of 13 shown Cities in severe |
| :---: | :---: | :---: | :---: | :---: |

![][image1]

Figure 1: Overview dashboard — national KPIs, city map, and severity distribution

The overview dashboard immediately reveals two structural features of India's air quality crisis. First, the distribution is extremely skewed: 84.62% of observations fall in the Moderate (31–60 µg/m³) band, while 15.38% reach the Unhealthy (61–150 µg/m³) band — and the very worst hours spike to nearly 40 times the WHO safe limit. Second, the crisis is geographically concentrated: just 8 of 29 cities account for the majority of severe-day observations, with Gurugram and Delhi as clear outliers.

## 

## **Temporal analysis — when does pollution peak?**

![][image2]

Figure 2: Temporal analysis dashboard — rolling trend, seasonal heatmap, monthly box plots

PM2.5 follows a consistent U-shaped annual cycle across all cities. Levels are at their lowest during the monsoon (July–August), when rainfall suppresses particulate accumulation. The critical rise begins in October post-monsoon and peaks in January. The 30-day rolling average confirms that the 2022 winter was the single worst period in the dataset, with January 2022 recording the highest observed monthly mean.

The seasonal heatmap reveals significant city-level heterogeneity. Agartala, for instance, peaks at 72.82 µg/m³ in Winter but falls to 17.65 in Monsoon — a four-fold seasonal swing. Aizawl, by contrast, remains comparatively stable across all seasons, suggesting local topography and lower industrial activity are protective factors.

## 

## **City comparison — spatial inequalities**

![][image3]

Figure 3: City comparison dashboard — ranked bar chart, risk scatter, and cluster analysis

The ranked bar chart confirms Gurugram (78.71 µg/m³) and Delhi (56.29 µg/m³) as the top two most polluted cities, well above the Indian average of 34.74 µg/m³ marked by the dashed reference line. The cluster scatter plot (Coefficient of Variation vs. Average PM2.5) is the most analytically rich visualisation in this section: it exposes four distinct city archetypes.

* High Avg, High Var (e.g., Mumbai, Kolkata): chronically polluted and volatile — episodes can be much worse than the average suggests.

* High Avg, Low Var (e.g., Delhi, Gurugram): persistently polluted — intervention must address structural emissions, not just episodic events.

* Low Avg, High Var (e.g., Aizawl, Imphal): generally clean but susceptible to occasional spikes from agricultural burning or meteorological anomalies.

* Low Avg, Low Var (e.g., Thiruvananthapuram, Goa): consistently clean — effective baselines for comparison.

## 

## **Meteorological drivers — interaction analysis**

![][image4]

Figure 4: Drivers dashboard — wind-humidity interaction heatmap and severe probability chart

The interaction heatmap and probability chart deliver the project's most operationally significant finding: the combination of Low Wind and High Humidity is not just marginally worse — it produces the highest severe pollution probability at approximately 0.12%, nearly double the probability under Low Wind \+ Low Humidity conditions. This is consistent with the atmospheric mechanism: calm, moist air allows particulates to accumulate without dispersal, and humidity promotes secondary aerosol formation.

Critically, season outweighs the wind-humidity combination as a PM2.5 predictor. The same Low Wind \+ High Humidity condition produces approximately 60 µg/m³ in Winter but only 20–25 µg/m³ in Monsoon. This means meteorological early warnings are most valuable when issued in winter, when background pollution levels are already elevated.

## 

## **Event impact analysis**

![][image5]

Figure 5: Event impact dashboard — scatter plot, event vs. non-event comparison, seasonal heatmap

The event analysis confirms that pollution spikes are event-driven rather than random. Festival periods record the highest average PM2.5 and the strongest positive event delta, followed closely by crop burning. The event vs. non-event comparison shows an average gap of 15–20%, with an impact spread of 28.89 µg/m³ above baseline. Post-monsoon season amplifies the impact of both event types, because the atmospheric mixing that suppresses accumulation during monsoon has already ended.

**9\.  Statistical Analysis**

## **Extreme event analysis**

![][image6]

Figure 6: Extreme events dashboard — seasonal concentration, probability ranking, and critical quadrant

The extreme events analysis (PM2.5 \> 250 µg/m³) recorded 740 qualifying events across the dataset, with an average extreme probability of 0.71%. Winter is the dominant season: it accounts for the majority of extreme events across nearly every city. The key insight from the scatter plot in Figure 6 is that no city falls in the Sudden Risk quadrant (low count, high probability) — instead, Gurugram and Delhi occupy the Critical quadrant (high count, high probability), confirming that their extreme events are structurally embedded rather than random.

## **PM2.5 forecasting — Random Forest model**

A dedicated prediction pipeline was implemented separately from the EDA layer (python cli.py \--predict \--city \<Name\>). The model uses a Random Forest Regressor trained on seven features: PM2.5 lags at 1h, 24h, and 168h; 24-hour rolling mean; wind speed; humidity; and temperature.

**Training methodology:**

* Time-ordered train/test split: the last 20% of chronological rows per city are held out for evaluation, ensuring no future data contaminates the training set.

* Multi-horizon targets: separate models are trained for each horizon (1h, 6h, 12h, 24h, 48h) by shifting the PM2.5 column forward by h steps as the target.

* Label leakage prevention: training rows are restricted to positions where the corresponding target falls strictly within the training window, preventing any test-period information from entering the feature set.

**Key model results (Delhi, indicative):**

| \> 0.85 1h horizon R² | \> 0.70 6h horizon R² | \> 0.55 24h horizon R² | \> 0.40 48h horizon R² |
| :---: | :---: | :---: | :---: |

Performance degrades gracefully with horizon length, as expected. Short-horizon forecasts (1–6 hours) are suitable for real-time public health advisories. The 24–48 hour forecasts provide sufficient lead time for industrial pre-compliance measures and school or event cancellations.

## **Segmentation and clustering**

The city cluster analysis (Figure 3\) constitutes an informal segmentation: cities are positioned in a two-dimensional space of Average PM2.5 vs. Coefficient of Variation. This reveals four regime types that require fundamentally different policy responses — structural emission controls for the High Avg/Low Var cluster versus event-response protocols for the High Var cities.

## **Autocorrelation and lag structure**

Lag correlation analysis on the Delhi time series (computed in src/analysis/temporal.py) confirms strong autocorrelation at lags of 1h, 24h, and 168h — the same lags used as model features. This validates the feature selection rationale: PM2.5 has memory at hourly, daily, and weekly timescales, reflecting emission cycles, boundary layer dynamics, and weekly activity patterns.

**10\.  Tableau Dashboard Design**

The Tableau dashboard is published at: [Tableau Dashboard Link](https://public.tableau.com/app/profile/yashi.agarwal1143/viz/Air_Quality_Final_Workbook11_17774593482750/Dashboard1)

The dashboard is structured as a six-page analytical narrative, moving from the national overview to increasingly specific diagnostics. Each page answers a single analytical question and contains its own key insights panel.

| Page | Title | Question Answered | Key Interactive Elements |
| ----- | :---- | :---- | :---- |
| **1** | **Overview** | What is the overall air quality situation across India? | City filter, severity level filter, avg PM2.5 range |
| **2** | **Temporal Analysis** | When does pollution rise and fall? | Season, Year, City filters; rolling trend line |
| **3** | **City Comparison** | Which cities behave differently? | City dropdown; cluster scatter, ranked bar |
| **4** | **Drivers** | What meteorological conditions amplify pollution? | Season and wind-humidity combination filters |
| **5** | **Event Impact** | Do events actually worsen pollution? | Event Type, Event Category, Season filters |
| **6** | **Extreme Events** | Where and when are severe events concentrated? | City, Risk level, Season filters |

**11\.  Insights Summary**

The following ten insights are stated in decision language — each tells the reader what to conclude and what action it implies.

**1\. Gurugram is a structural emergency, not an episodic problem.**

With an annual average PM2.5 of 78.71 µg/m³ — nearly twice the Indian average — and the highest extreme event count and probability of any city, Gurugram's pollution is a year-round chronic condition. Standard event-response protocols are insufficient; structural industrial and vehicular emission controls are required.

**2\. Delhi and the NCR cluster need coordinated governance.**

Delhi (56.29 µg/m³), Gurugram, Patna, and Kolkata form a critical quadrant in which both event frequency and probability are simultaneously above average. These cities share airshed boundaries and atmospheric transport pathways, meaning local interventions alone are insufficient without regional coordination.

**3\. Winter is the only season that matters for extreme-event planning.**

Of the 740 total extreme pollution events, the vast majority occur in November–January. Emergency protocols, school closures, industrial restrictions, and public health advisories should be designed as winter-specific, with automatic activation when meteorological forecasts indicate stagnation.

**4\. Low wind plus high humidity is the highest-risk weather state.**

This combination produces approximately 0.12% severe pollution probability — nearly double the probability under any other weather combination. Meteorological early-warning systems that flag this combination in winter can provide 6–24 hours of actionable lead time.

**5\. The monsoon provides a natural pollution reprieve — and a planning window.**

PM2.5 reaches its annual minimum in July–August across all cities. This period should be used for infrastructure maintenance, sensor calibration, and pre-season enforcement preparation, not treated simply as a low-priority operational period.

**6\. Festivals amplify pollution more than any other single event type.**

Festival periods record the highest average PM2.5, the strongest event delta, and the greatest impact spread above baseline. Restricting open-air fireworks and regulating festival-related vehicle movement and bonfires would directly reduce the most impactful pollution spikes.

**7\. Crop burning is a systemic post-monsoon risk driver.**

Crop burning maintains consistently high PM2.5 levels through October–November, compounding the seasonal rise that begins post-monsoon. Enforcement of the existing stubble-burning ban — with satellite monitoring — is the highest-leverage post-monsoon intervention available to state governments.

**8\. Cities with similar averages can have vastly different risk profiles.**

The cluster analysis reveals that CV (volatility) is as important as average PM2.5 for policy design. Mumbai and Kolkata have similar averages but high variability — their worst days are much worse than their averages suggest, requiring episode-response infrastructure that static average-based monitoring would miss.

**9\. Short-horizon PM2.5 forecasts are operationally viable.**

The Random Forest model achieves R² \> 0.85 at the 1-hour horizon and \> 0.40 at 48 hours for Delhi, using only seven publicly available meteorological and lag-based features. This demonstrates that a deployable early-warning system is feasible without exotic data sources.

**10\. Air quality in India is not uniformly bad — it is structurally concentrated.**

Seven of 13 cities studied exceed the severe threshold on a meaningful share of days. The remaining cities are substantially cleaner and provide proof of concept that urban air quality management at scale is achievable within India's existing policy and governance framework.

**12\.  Recommendations**

**Recommendation 1: Implement a Winter Air Quality Emergency Protocol in the NCR cluster**

**Insight basis:** Insights 1, 2, 3, 4

Cities in the critical quadrant (Gurugram, Delhi, Kolkata, Patna) should activate a structured emergency protocol each year from 15 October, triggered automatically by SAFAR or IMD meteorological forecasts projecting Low Wind \+ High Humidity conditions. The protocol should include graded responses: Green (advisory), Amber (school closures, construction ban), Red (odd-even vehicle restrictions, industrial shutdowns). Existing GRAP (Graded Response Action Plan) frameworks in Delhi-NCR provide a legal and administrative template for extension to other cities.

| Expected impact: Reduces severe pollution days in the highest-exposure cities by an estimated 15–25% in winter months, directly benefiting approximately 30 million urban residents. |
| :---- |

**Recommendation 2: Enforce the stubble-burning ban with satellite monitoring and real-time penalty triggers**

**Insight basis:** Insights 6, 7

The existing ban on paddy stubble burning in Punjab, Haryana, and UP is widely flouted. Integrating NASA FIRMS satellite fire detection data with district-level enforcement dashboards would enable real-time violation identification and penalty dispatch. Paired with a viable alternative (subsidised happy seeders, biomass collection programmes), this approach addresses the root cause rather than the symptom.

| Expected impact: Estimated 10–15% reduction in post-monsoon PM2.5 in northern cities during October–November, when crop burning compounds the seasonal rise. |
| :---- |

**Recommendation 3: Deploy the PM2.5 forecasting model as a public early-warning service**

**Insight basis:** Insight 9

The Random Forest model developed in this project is operationally deployable as a REST API with minimal infrastructure: a Python FastAPI wrapper, a scheduled hourly data-feed from open meteorological APIs (e.g., Open-Meteo), and a WhatsApp or SMS notification layer for public alerts. This would provide 6–48 hour advance warnings to residents, hospitals, schools, and outdoor event organisers in high-risk cities.

| Expected impact: An operational forecasting service costs approximately INR 5–10 lakh per year in cloud infrastructure and is replicable across all 29 cities in this dataset without retraining. |
| :---- |

**Recommendation 4: Regulate open-air fireworks and festival emissions with city-specific event policies**

**Insight basis:** Insight 6

Festival-period restrictions (e.g., the Delhi green cracker policy) have demonstrated measurable impact. Extending these regulations city-by-city, with penalty enforcement and public communication campaigns tied to air quality index readings, would reduce the largest single episodic amplifier identified in this analysis.

| Expected impact: Potential 10–20% reduction in peak festival-period PM2.5 concentrations in cities with high festival-season event deltas. |
| :---- |

**Recommendation 5: Standardise the use of the Coefficient of Variation as a reporting metric alongside the average PM2.5**

**Insight basis:** Insight 8

Current public reporting — including CPCB dashboards — focuses almost exclusively on daily and annual average PM2.5. Cities with high CV are systematically under-flagged by average-based metrics: their worst days are far worse than their averages suggest. Mandating CV reporting alongside averages in national and state air quality annual reports would improve resource allocation and risk communication.

| Expected impact: Administrative cost near zero; significantly improves the signal value of existing monitoring infrastructure. |
| :---- |

**13\.  Impact Estimation**

The following estimates use conservative assumptions and publicly available data. They are order-of-magnitude figures intended to illustrate the decision logic, not precise financial projections.

| Recommendation | Type of Impact | Estimated Magnitude | Time to Impact |
| :---- | :---- | :---- | :---- |
| **Winter Emergency Protocol** | Public health/risk reduction | 15–25% reduction in severe winter days in 4 cities; \~30M residents benefited | 1–2 winters post-implementation |
| **Stubble burning ban enforcement** | Efficiency gain/emission reduction | 10–15% PM2.5 reduction Oct–Nov in northern cities | 1 agricultural season |
| **Forecasting early-warning service** | Risk reduction/cost avoidance | INR 5–10L deployment cost; avoided hospital admissions estimated at 10–50x return | 3–6 months to deploy |
| **Festival emission regulation** | Emission reduction | 10–20% peak reduction during festival windows in regulated cities | 1 festival season |
| **CV reporting standardisation** | Efficiency / improved targeting | Improved resource allocation — no direct cost; near-zero implementation cost | Immediate on policy adoption |

The urgency case: India's air quality crisis is already costing the country an estimated USD 150 billion per year in health and productivity losses (World Bank, 2022). The recommendations above address the highest-leverage, most evidence-backed intervention points identified in this data. The cost of inaction — measured in hospital admissions, school absences, and reduced life expectancy — substantially exceeds the cost of implementation.

**14\.  Limitations**

## **Data gaps and quality issues**

* Coverage gaps: sensor downtime during monsoon months for several cities means the cleanest season may be slightly underrepresented in some city-level averages.

* Urban bias: all 29 cities are major urban or industrial centres. The dataset cannot be used to draw conclusions about rural or peri-urban air quality, where exposure patterns and emission sources differ substantially.

* Single pollutant: only PM2.5 is modelled. Ozone, NO2, and CO all contribute to health risk and follow different seasonal and meteorological patterns; their exclusion means the analysis understates total air quality risk in summer months when photochemical smog is prevalent.

## **Assumptions that may not hold universally**

* Festival and crop-burning flags are calendar-derived. The actual intensity and spatial extent of these events vary year to year; the binary flag does not capture variation in event severity.

* The Low Wind threshold of \< 5 km/h and High Humidity threshold of \> 70% were set as fixed engineering assumptions. The precise thresholds that maximise meteorological prediction accuracy may differ by city and season.

* The forecasting model was validated primarily on Delhi. Generalisation to all 29 cities requires per-city validation, which was not performed at scale due to computational scope.

## **What cannot be concluded from this analysis?**

* Causality: the analysis identifies strong associations between meteorological conditions, events, and PM2.5 concentrations, but does not establish causal pathways. For example, it cannot distinguish between crop burning directly causing PM2.5 spikes and both crop burning and high PM2.5 being independently caused by post-monsoon meteorological conditions.

* Health impact: This analysis measures PM2.5 concentration, not population exposure or health outcomes. Translating concentration data into health impact estimates requires additional demographic, epidemiological, and spatial modelling.

**15\.  Future Scope**

## **Additional analysis with more data**

* Multi-pollutant modelling: integrating NO2, O3, CO, and SO2 data would enable a full AQI calculation and more accurate health risk estimation, particularly for summer months when PM2.5 is lower but photochemical pollutants are elevated.

* Satellite-derived PM2.5: NASA MODIS and Sentinel-5P satellite data can provide continuous national coverage, filling the urban sensor bias and enabling rural and peri-urban analysis.

* Health outcome linkage: correlating city-level PM2.5 patterns with hospital admission data (respiratory and cardiovascular) would move the analysis from exposure characterisation to health impact quantification.

## **New data sources that would strengthen findings**

* IMD meteorological gridded data: replacing point-sensor wind and humidity readings with gridded model output would improve the spatial resolution and accuracy of the meteorological driver analysis.

* FIRMS satellite fire detection: real-time crop burning event identification would replace the calendar-derived binary flag with a continuous, spatially explicit emission intensity measure.

* Traffic density and industrial activity data: adding emissions proxies would enable source attribution modelling.

## **Predictive and real-time extensions**

* A real-time Tableau or Power BI dashboard connected to a live meteorological API and the deployed forecasting model would transform this analytical project into an operational public health infrastructure tool.

* Deep learning approaches (LSTM, Transformer) on the full multi-city time series could improve forecast accuracy at the 24–48 hour horizon, where the Random Forest performance degrades.

* A city-specific alert API with WhatsApp and SMS integration could deliver actionable early warnings directly to residents, hospitals, and schools within the existing technology infrastructure of Indian municipalities.

**16\.  Conclusion**

India's air quality crisis is real, measurable, and — crucially — structured. This project analysed more than 800,000 hourly PM2.5 observations across 29 cities to demonstrate that dangerous pollution is not uniformly distributed in time or space: it concentrates in winter, in a handful of northern cities, under specific meteorological conditions, and around predictable calendar events. Using a reproducible Python pipeline, a six-page interactive Tableau dashboard, and a validated Random Forest forecasting model, this team has produced a comprehensive analytical platform that moves beyond describing the problem to diagnosing its causes and enabling its anticipation. The most important recommendation is also the most actionable: deploy a winter emergency protocol in Gurugram, Delhi, Kolkata, and Patna, triggered by meteorological forecasts of the Low Wind \+ High Humidity conditions identified in this analysis as the single most dangerous weather state. This would be the highest-leverage, lowest-cost policy intervention supported by the data, and it could be implemented within a single policy cycle.

**17\.  Appendix**

## **A. Data dictionary — full column definitions**

| Column name | Data type | Unit | Full definition |
| :---- | :---- | :---- | :---- |
| **Datetime** | DateTime | — | Hourly timestamp in ISO 8601 format; parsed to pandas datetime on ingestion |
| **City** | String | — | Name of Indian city; 29 unique values in this dataset |
| **PM2\_5\_ugm3** | Float64 | µg/m³ | PM2.5 particulate concentration; values \< 0 removed in cleaning; \> 250 flagged as severe |
| **Humidity\_Percent** | Float64 | % | Relative humidity; clipped to 0–100 in cleaning; \> 70% flagged as high\_humidity |
| **Wind\_Speed\_10m\_kmh** | Float64 | km/h | Wind speed at 10m height; negative values converted to absolute; \< 5 flagged as low\_wind |
| **Temp\_2m\_C** | Float64 | °C | Air temperature at 2m height; used as a forecasting feature |
| **Season** | String | — | One of: Winter (Dec–Feb), Summer (Mar–May), Monsoon (Jun–Sep), Post-Monsoon (Oct–Nov) |
| **Festival\_Period** | Integer | 0/1 | 1 if date falls within a recognised Indian festival calendar period; 0 otherwise |
| **Crop\_Burning\_Season** | Integer | 0/1 | 1 if date falls within agricultural crop residue burning season; 0 otherwise |
| **Latitude** | Float64 | degrees | City centroid latitude for geographic visualisation |
| **Longitude** | Float64 | degrees | City centroid longitude for geographic visualisation |
| **pm25\_lag\_1** | Float64 | µg/m³ | PM2.5 value from 1 hour prior for the same city; NaN for the first row per city |
| **pm25\_lag\_24** | Float64 | µg/m³ | PM2.5 value from 24 hours prior for the same city |
| **pm25\_lag\_168** | Float64 | µg/m³ | PM2.5 value from 168 hours (7 days) prior to the same city |
| **pm25\_roll\_24** | Float64 | µg/m³ | 24-hour rolling mean of PM2.5 per city |
| **pm25\_roll\_std\_24** | Float64 | µg/m³ | 24-hour rolling standard deviation of PM2.5 per city |
| **pm25\_deviation** | Float64 | µg/m³ | PM2.5 minus pm25\_roll\_24; measures deviation from local baseline |
| **pm25\_category** | String | — | Indian AQI-style category: Good (0–30), Satisfactory (31–60), Moderate (61–90), Poor (91–120), Very Poor (121–250), Severe (\>250) |
| **is\_severe** | Boolean | — | True if PM2\_5\_ugm3 \> 250; used as a target in extreme event analysis |
| **low\_wind** | Boolean | — | True if Wind\_Speed\_10m\_kmh \< 5; meteorological stagnation indicator |
| **high\_humidity** | Boolean | — | True if Humidity\_Percent \> 70; atmospheric accumulation indicator |
| **is\_festival** | Boolean | — | Cast from Festival\_Period \== 1 |
| **is\_crop\_burning** | Boolean | — | Cast from Crop\_Burning\_Season \== 1 |
| **year/month/hour** | Integer | — | Extracted from Datetime for temporal segmentation |
| **day\_of\_week** | Integer | 0–6 | 0 \= Monday; used to capture weekly emission cycles |

## **B. Python pipeline — key module reference**

| Module | Role in pipeline |
| :---- | :---- |
| src/ingestion/loader.py | Reads config.yaml, resolves raw CSV path, loads and parses Datetime |
| src/preprocessing/validation.py | Schema, range, and duplicate checks — non-destructive, logs issues only |
| src/preprocessing/cleaning.py | Removes invalid rows, clips/corrects out-of-range values, sorts time series |
| src/preprocessing/feature\_engineering.py | Adds lags, rolling stats, calendar features, severity flags, and event indicators |
| src/analysis/profiling.py | Global distribution stats, tail risk, missingness, per-city summaries |
| src/analysis/temporal.py | Daily/monthly aggregates, rolling trends, autocorrelation, diurnal and seasonal patterns |
| src/analysis/interactions.py | Wind × season, humidity × season, severe probability by weather group |
| src/analysis/events.py | Festival and crop-burning impact vs. rolling baseline |
| src/analysis/extremes.py | Severe event distribution by city/season, conditional extreme probability |
| src/analysis/forecasting.py | Multi-horizon Random Forest training, time-split metrics, joblib model saving |
| src/analysis/synthesis.py | Builds Tableau-ready dashboard CSVs (--stage full only) |
| cli.py | Main CLI: \--stage for EDA, \--predict for forecasting |

**18\.  Contribution Matrix**

The table below documents each team member's contribution across all project phases. Contributions are verifiable through GitHub Insights, PR history, and committed files at https://github.com/3ncryptor/DVA\_Capstone\_2.

| Team Member | Dataset & Sourcing | ETL & Cleaning | EDA & Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT & Viva |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Yashi Agarwal** | Yes | — | — | Yes | Yes | — | — |
| **Vani Rudra** | Yes | — | — | Yes | Yes | — | — |
| **Satya Yadav** | Yes | — | — | Yes | Yes | — | — |
| **Rohit Kumar** | — | — | Yes | Yes | Yes | — | — |
| **Mohan Kumar CR** | — | — | Yes | Yes | Yes | — | — |
| **Aryan Vibhuti** | — | Yes | Yes | Yes | — | Yes | Yes |

Declaration: We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artefacts.

Team Lead Signature: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Date: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

