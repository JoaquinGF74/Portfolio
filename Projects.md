---
layout: default
---

# Projects

With a strong foundation in data analytics, I specialize in transforming complex datasets into actionable insights that support strategic decision-making. I’ve led diverse projects across industries, applying advanced techniques in machine learning (using Python and R), writing optimized SQL queries, and building predictive models. My experience also includes designing interactive dashboards and compelling visualizations in Power BI and Tableau, effectively turning raw data into meaningful business intelligence. Below is a curated selection of my most impactful projects, showcasing my skills in statistical analysis, predictive modeling, and data storytelling.

---

## [COVID Statistics Analysis between 2020 & 2021](./Projects/covid-project-2020-2021/covid-statistics-2020-2021.md)

This project analyzes data collected by the World Health Organization between 2020 and 2021.

### Key Steps:

- **Data Collection:** Downloaded the COVID-19 dataset from the World Health Organization.
- **Data Cleaning & Transformation:** Processed missing values, created key fields, and standardized formats.
- **Visualization & Analysis:** Built an interactive dashboard to analyze global statistics, percentage of population infected, and forecasted average infection rates.
- **Insights Extraction:** Identified infection trends, country-specific results, and local responses to the pandemic.

**Technologies:** `SQL`, `Excel`, `Tableau`

**Key Insight:** Uses a forecasting model to provide valuable insights based on each country's situation, allowing for preventive measures based on expected outcomes.

---

## [State Sale Profitability by City (2018–2021)](./Projects/sales-profit-project/sales-profit-across-the-usa.md)

This project classifies sales data by category and segment across the United States (e.g., Technology, Furniture, etc.).

### Key Steps:

- **Data Collection:** Imported sales data and prepared it for analysis in Tableau.
- **Data Cleaning & Transformation:** Cleaned the dataset and connected multiple tables from the data source.
- **Visualization & Analysis:** Built an interactive dashboard to analyze national profitability trends and product-level revenue.
- **Insights Extraction:** Identified seasonal patterns, potential market expansion areas, and revenue growth opportunities.

**Technologies:** `Excel`, `Tableau`

**Key Insight:** Utilizes key performance indicators to assess market profitability and guide strategic product placement across regions.

---

## [Banking Ledger and Fraud Detection System](./Projects/banking-ledger/fraud-detection-notebook.md)

This project simulates a digital banking environment, models user and transaction behavior in a relational MySQL database, and implements fraud detection using machine learning.

### Key Steps:

- **Data Generation:** Created realistic user, account, and transaction data using Python and Faker to simulate a full banking ledger.
- **Database Design & ETL:** Designed and populated a MySQL relational schema (`Users`, `Accounts`, `Transactions`), with time-stamped entries and cross-referenced relationships.
- **Fraud Detection Modeling:** Built a Python-based notebook that applies multiple rules (e.g., high frequency, failed attempts, outlier amounts) to detect fraudulent transactions.
- **Visualization & Dashboarding:** Designed a Power BI dashboard with dedicated fraud indicators and KPI metrics to explore high-risk patterns and anomalies.
- **Insights Extraction:** Flagged suspicious users and transaction trends by time, value, and activity patterns to aid in fraud prevention and monitoring.

**Technologies:** `MySQL`, `Python`, `pandas`, `Power BI`

**Key Insight:** Combines rule-based anomaly detection and data storytelling to highlight financial fraud patterns and support risk assessment with interactive visual tools.

## [Athlete Performance & Injury-Risk Analytics](./Projects/athlete-performance-analytics/athlete-performance-analytics.md)

This project builds an end-to-end athlete monitoring system for a college rugby team, simulating training data and computing injury-risk scores in a live-connected pipeline.

### Key Steps:

- **Data Pipeline:** Built a Python ETL pipeline generating realistic training/match session data, written directly into PostgreSQL.
- **Database Design:** Designed a normalized PostgreSQL schema (`Players`, `Sessions`, `PlayerRiskScore`) queried live by Power BI, with no CSV hand-off.
- **Injury-Risk Modeling:** Implemented the Acute:Chronic Workload Ratio (ACWR) methodology to flag players as low, moderate, or high risk of injury.
- **Visualization & Analysis:** Built a DirectQuery-connected Power BI dashboard with KPI cards, risk breakdowns, and a live high-risk player table.

**Technologies:** `Python`, `PostgreSQL`, `Power BI`

**Key Insight:** Differentiating forwards from backs in the workload model reveals distinct ACWR profiles by position, showing the dashboard catching real positional workload patterns rather than flat, undifferentiated risk scores.

---

### [Back](./)
