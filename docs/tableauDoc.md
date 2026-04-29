# Multi-Page Tableau Dashboard — Implementation Plan

A practical build guide for the seven-page Tableau workbook that consumes the
project's CSV exports and the prediction CLI output. Each page is built from a
single, purpose-built dataset (no joins) and answers exactly one analytical
question.

---

## Table of Contents

1. [Overall Architecture](#0-overall-architecture)
2. [Tableau Setup](#1-tableau-setup)
3. [Page 1 — Overview](#page-1--overview)
4. [Page 2 — Temporal Analysis](#page-2--temporal-analysis)
5. [Page 3 — City Comparison](#page-3--city-comparison)
6. [Page 4 — Drivers](#page-4--drivers)
7. [Page 5 — Event Impact](#page-5--event-impact)
8. [Page 6 — Extreme Events](#page-6--extreme-events)
9. [Page 7 — Prediction](#page-7--prediction)
10. [Global Filters](#global-filters)
11. [Actions and Interactivity](#actions-and-interactivity)
12. [Formatting Rules](#formatting-rules)
13. [Final Validation Checklist](#final-validation-checklist)

---

## 0. Overall Architecture

### Objective

Build a **seven-page analytical dashboard** that walks the viewer through the
following narrative:

```text
What  ->  When  ->  Where  ->  Why  ->  Trigger  ->  Risk  ->  Future
```

### Data Sources (Final Inputs)

Import only the CSV exports produced by the EDA pipeline plus the prediction
output rendered to CSV from the CLI run summary:

```text
overview_dashboard.csv
temporal_dashboard.csv
city_dashboard.csv
interaction_dashboard.csv
events_dashboard.csv
extremes_dashboard.csv
prediction_output.csv      (derived from the CLI / last_run.json)
```

### Critical Rules

| Rule | Status |
| --- | --- |
| Do **not** join datasets initially | Required |
| Do **not** import the raw dataset | Required |
| Use a **separate data source per page** | Required |

---

## 1. Tableau Setup

### Step 1 — Import Data

In Tableau:

```
Data  ->  New Data Source  ->  Text File
```

Import all six dashboard CSVs (and the prediction CSV when ready).

### Step 2 — Rename Data Sources

| Original                | Rename To  |
| ----------------------- | ---------- |
| `overview_dashboard`    | `Overview` |
| `temporal_dashboard`    | `Temporal` |
| `city_dashboard`        | `City`     |
| `interaction_dashboard` | `Drivers`  |
| `events_dashboard`      | `Events`   |
| `extremes_dashboard`    | `Extremes` |

### Step 3 — Data Type Check

Confirm that Tableau infers the correct types:

| Field      | Type    |
| ---------- | ------- |
| City       | String  |
| Date       | Date    |
| Season     | String  |
| PM values  | Number  |
| Flags      | Boolean |

---

## Page 1 — Overview

**Data source:** `overview_dashboard.csv`
**Goal:** Provide a high-level snapshot of national air quality.

### Sheets

#### 1. KPI Cards (three sheets)

**Fields**

- `avg_pm25`
- `max_pm25`
- `severe_pct`

**Build**

- Drag the measure to **Text**.
- Use a large title font (40–60 pt).
- Apply color via a calculated field:

```tableau
IF [avg_pm25] < 60 THEN "Good"
ELSEIF [avg_pm25] < 150 THEN "Moderate"
ELSE "Severe"
END
```

#### 2. Map

**Fields**

- `City`     -> Detail
- `lat`      -> Latitude
- `lon`      -> Longitude
- `avg_pm25` -> Color
- `max_pm25` -> Size

**Steps**

- Set **Mark type** to *Circle*.
- Color gradient: green (low) to red (high).

#### 3. Mini Trend (optional)

Use the **Temporal** dataset (a dual-source layout is acceptable for this
single sheet).

### Dashboard Layout

| Region | Content     |
| ------ | ----------- |
| Top    | KPI cards   |
| Center | Map         |
| Bottom | Mini trend  |

---

## Page 2 — Temporal Analysis

**Data source:** `temporal_dashboard.csv`
**Goal:** Explain the time-domain behaviour of PM2.5.

### Sheets

#### 1. Time Series

**Fields**

- `date`         -> Columns
- `pm25_avg`     -> Rows
- `rolling_pm25` -> Dual axis

**Steps**

- Add `rolling_pm25` as a dual axis.
- Synchronise both axes.
- Render the rolling line as a dashed line.

#### 2. Seasonal Heatmap

**Fields**

- `City`     -> Rows
- `Season`   -> Columns
- `pm25_avg` -> Color

**Steps**

- Set **Mark type** to *Square*.
- Apply a continuous gradient.

#### 3. Diurnal Pattern (when available)

**Fields**

- `hour`  -> Columns
- `PM2.5` -> Rows

#### 4. Monthly Box Plot (optional)

### Dashboard Layout

| Region       | Content      |
| ------------ | ------------ |
| Top          | Time series  |
| Bottom-left  | Heatmap      |
| Bottom-right | Diurnal      |

---

## Page 3 — City Comparison

**Data source:** `city_dashboard.csv`
**Goal:** Compare cities across central tendency and dispersion.

### Sheets

#### 1. Ranked Bar Chart

**Fields**

- `City` -> Rows
- `mean` -> Columns

**Steps**

- Sort descending.
- Color the bars by `mean`.

#### 2. Box Plot

Build only if a per-city distribution is available; otherwise skip.

#### 3. CV vs. Mean Scatter (advanced)

**Fields**

- `mean` -> X
- `cv`   -> Y
- `City` -> Label

#### 4. Cluster Chart (only if clustering has been added upstream)

### Dashboard Layout

| Region | Content    |
| ------ | ---------- |
| Left   | Bar chart  |
| Right  | Box plot   |
| Bottom | Scatter    |

---

## Page 4 — Drivers

**Data source:** `interaction_dashboard.csv`
**Goal:** Explain *why* PM2.5 increases under specific conditions.

### Sheets

#### 1. Interaction Heatmap

**Fields**

- `low_wind`       -> Columns
- `high_humidity`  -> Rows
- `pm25_avg`       -> Color

#### 2. Seasonal Condition Comparison

**Fields**

- `Season`   -> Columns
- `pm25_avg` -> Rows
- `Condition` -> Color

#### 3. Severe Probability Chart

**Fields**

- `Condition`           -> Columns
- `severe_probability`  -> Rows

### Dashboard Layout

| Region | Content      |
| ------ | ------------ |
| Left   | Heatmap      |
| Right  | Bars         |
| Bottom | Probability  |

---

## Page 5 — Event Impact

**Data source:** `events_dashboard.csv`
**Goal:** Validate the impact of festivals and crop-burning episodes.

### Sheets

#### 1. Event vs. Non-Event

**Fields**

- `event_type` -> Columns
- `pm25_avg`   -> Rows

#### 2. Event Delta

**Fields**

- `event_type`  -> Columns
- `event_delta` -> Rows

#### 3. Severity Probability

**Fields**

- `event_type`         -> Columns
- `severe_probability` -> Rows

### Dashboard Layout

Three charts placed side-by-side on a single horizontal row.

---

## Page 6 — Extreme Events

**Data source:** `extremes_dashboard.csv`
**Goal:** Identify which cities and seasons concentrate extreme-pollution risk.

### Sheets

#### 1. Heatmap

**Fields**

- `City`          -> Rows
- `Season`        -> Columns
- `extreme_count` -> Color

#### 2. Extreme Probability

**Fields**

- `City`                -> Columns
- `extreme_probability` -> Rows

#### 3. Ranking Bar

**Fields**

- `City`          -> Rows
- `extreme_count` -> Columns

### Dashboard Layout

| Region | Content        |
| ------ | -------------- |
| Top    | Heatmap        |
| Bottom | Probability + ranking bars |

---

## Page 7 — Prediction

**Data source:** Custom CSV derived from the CLI prediction run
(`outputs/prediction/last_run.json`  ->  flat CSV).

### Expected Schema

```text
City | Horizon | Prediction | Risk
```

### Sheets

#### 1. Prediction Table

- Horizons: 24 h, 48 h, 72 h (extend as needed).
- Prediction values per city and horizon.

#### 2. Risk Indicator

Calculated field used to colour-code the Risk column:

```tableau
IF [Prediction] > 250 THEN "Severe"
ELSEIF [Prediction] > 120 THEN "Poor"
ELSE "Moderate"
END
```

#### 3. SHAP Bar Chart (optional)

Add only if explainability data is exported alongside the predictions.

### Dashboard Layout

A centred, card-style layout that emphasises the predicted values and the
associated risk badge.

---

## Global Filters

Add the following filters to **every page**:

- `City`
- `Season`
- `Year`

**Steps**

1. Add the filter on any sheet.
2. Right-click the filter -> **Apply to Worksheets** -> **All Using Related
   Data**.

---

## Actions and Interactivity

### 1. City Click Action

- **Source sheets:** Map and ranked bar charts.
- **Target sheets:** All sheets across the workbook.

### 2. Hover Tooltips

Tooltips should expose at minimum:

- `avg_pm25`
- Severe percentage
- Latest prediction (where available)

---

## Formatting Rules

### Colors

| Value  | Color  |
| ------ | ------ |
| Low    | Green  |
| Medium | Yellow |
| High   | Orange |
| Severe | Red    |

### Fonts

| Element | Style       |
| ------- | ----------- |
| Titles  | Bold        |
| Labels  | Light grey  |
| Values  | White       |

---

## Final Validation Checklist

Run through this list before delivering the workbook:

- [ ] Filters propagate correctly across all pages.
- [ ] No blank or broken charts.
- [ ] Consistent color scheme across pages.
- [ ] Every chart title states the question it answers.
- [ ] Each page answers exactly one analytical question.

---

*End of document.*
