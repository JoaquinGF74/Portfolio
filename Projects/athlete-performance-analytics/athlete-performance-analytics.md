# **Athlete Performance & Injury-Risk Analytics**

![Athlete Performance & Injury-Risk Analytics](https://raw.githubusercontent.com/JoaquinGF74/Portfolio/main/assets/athlete_performance_dashboard_img.png)

### **Project Overview**

This project builds an end-to-end athlete monitoring system for a college rugby team, combining **Python**, **PostgreSQL**, and **Power BI**. The goal was to simulate realistic training and match data, compute injury-risk scores using an established sports-science model, and surface the results in a live, DirectQuery-connected Power BI dashboard that coaching staff could use to spot at-risk players before they get hurt.

# **Objectives**

- **Data Pipeline:** Build a Python ETL pipeline that generates realistic training/match session data and writes it directly into a PostgreSQL database.
- **Injury-Risk Modeling:** Implement the Acute:Chronic Workload Ratio (ACWR) methodology to flag players as low, moderate, or high risk of injury based on rolling training load.
- **Database Design:** Design a normalized PostgreSQL schema (`Players`, `Sessions`, `PlayerRiskScore`) that Power BI can query directly, with no manual CSV hand-off.
- **Interactive Dashboard:** Develop a Power BI DirectQuery dashboard so risk data stays current every time the pipeline runs, with no manual refresh step.

## **Methodology**

### 1. Synthetic Data Generation (Python)

- Used `numpy`'s random generators to simulate 80 players across 10 rugby positions, generating realistic training/match session data (duration, RPE, distance covered, high-speed running).
- Differentiated forwards from backs when generating distance and high-speed running metrics, reflecting the real positional split in workload between forwards (set-piece, collision-focused) and backs (running-focused) roles.
- Built idempotent `INSERT ... ON CONFLICT ... DO UPDATE` upserts so the pipeline can be safely rerun to accumulate new weeks of history without duplicating past sessions.

### 2. PostgreSQL Database Design

- Designed a relational schema connected directly via `psycopg2`, with `Sessions` and `PlayerRiskScore` both referencing `Players` by foreign key.

```sql
CREATE TABLE Players (
	player_id		SERIAL PRIMARY KEY,
	full_name		VARCHAR(100) NOT NULL,
	position		VARCHAR(30) NOT NULL,
	team			VARCHAR(50) NOT NULL,
	date_of_birth	DATE
);

CREATE TABLE Sessions (
	session_id			SERIAL PRIMARY KEY,
	player_id			INT NOT NULL REFERENCES Players(player_id),
	session_date		DATE NOT NULL,
	session_type		VARCHAR(20) NOT NULL,
	duration_minutes	INT NOT NULL,
	rpe					SMALLINT NOT NULL,
	distance_km			DECIMAL(5,2),
	high_speed_m		INT
);

-- Populated by the Python pipeline after computing ACWR + risk flags.
-- Power BI reads this table directly for the dashboard.
CREATE TABLE PlayerRiskScore (
	score_id			SERIAL PRIMARY KEY,
	player_id			INT NOT NULL REFERENCES Players(player_id),
	as_of_date			DATE NOT NULL,
	acute_workload		DECIMAL(8,2),
	chronic_workload	DECIMAL(8,2),
	acwr				DECIMAL(8,2),
	risk_flag			VARCHAR(20)
);
```

### 3. ACWR Injury-Risk Calculation

- Implemented the rolling-average ACWR method (Gabbett, 2016): acute workload (trailing 7-day load) divided by chronic workload (trailing 28-day average weekly load), where load = duration × RPE.
- Classified each player-date combination into risk bands using established sports-science thresholds, computed with `pandas` rolling windows grouped per player.

```python
acute = daily_load.rolling("7D").sum()
chronic_28d_total = daily_load.rolling("28D").sum()
chronic_weekly_avg = chronic_28d_total / 4
acwr = (acute / chronic_weekly_avg).replace([np.inf, -np.inf], np.nan)

# Risk bands (Gabbett, 2016):
#   ACWR <= 1.3          -> 'low'      (undertrained or the "sweet spot")
#   1.3 <  ACWR <= 1.5    -> 'moderate'
#   ACWR >  1.5            -> 'high'     (sharp spike in load, elevated injury risk)
```

### 4. Power BI Dashboard

- Connected Power BI directly to PostgreSQL via **DirectQuery**, so the dashboard reflects new pipeline runs live, with no manual refresh step.
- Built a star-schema data model (`Players` and a `DateTable` as dimension tables feeding `Sessions` and `PlayerRiskScore`) with DAX measures for current risk counts, average ACWR, and risk percentage.
- Designed a Team Overview page with KPI cards, a color-coded risk-flag breakdown donut, an ACWR-by-position bar chart with conditional formatting, and a live high-risk player table filtered to the most recent scoring date.

## Key Insights

- Forwards and backs show distinct workload profiles once positional differentiation was added to the data model: high-work-rate positions like Number 8 and Wing tend to carry the highest average ACWR, while Props and Fullbacks — whose training load is comparatively lower-intensity — sit at the lower end.
- At any given time, the large majority of the squad sits comfortably in the "low" risk band (ACWR between 0.8–1.3), which is exactly the pattern a well-managed training program should show, with only a small handful of players tipping into "moderate" or "high" after a spike in match-day intensity.
- Because Power BI connects live via DirectQuery, the dashboard requires zero manual maintenance to stay current — rerunning the Python pipeline is the only step needed to reflect a new week of training data.

### Technologies Used

- `Python`: Data pipeline, synthetic data generation, and ACWR calculation (`pandas`, `numpy`, `psycopg2`).
- `PostgreSQL`: Relational database design and live query source for Power BI.
- `Power BI`: DirectQuery data model, DAX measures, and interactive dashboard.

## Conclusion

This project combines data engineering, sports-science domain modeling, and BI dashboarding into a single working pipeline — from synthetic data generation, through injury-risk computation, to a live executive dashboard. Having played and captained Division 1 rugby, I built this project to apply the same workload-monitoring concepts real strength & conditioning staffs use, and to demonstrate how a small athletics program could adopt a low-cost, fully self-hosted alternative to commercial athlete-monitoring platforms. Moving forward, this pipeline could be extended with GPS-tracked session data, wellness/soreness questionnaires, and automated alerts when a player crosses into high-risk territory.

## Power BI Report:
[ACWR_Report.pbix](https://github.com/JoaquinGF74/Portfolio/raw/main/Projects/athlete-performance-analytics/ACWR_Report.pbix)

### [Back](https://joaquingf74.github.io/Portfolio/Projects.html)
