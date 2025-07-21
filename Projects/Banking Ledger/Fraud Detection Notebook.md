# **Banking Ledger and Fraud Detection System**

![Banking Ledger Dashboard](https://raw.githubusercontent.com/JoaquinGF74/Portfolio/main/assets/banking_fraud_dashboard_img.png)

### **Project Overview**

This project simulates a digital banking environment and applies **Machine Learning** to detect fraudulent activity. It combines **MySQL**, **Python**, and **Power BI** to build an end-to-end solution that handles transaction data generation, storage, fraud detection, and visualization.  

# **Objectives**

- **Data Simulation:** Generate realistic Users, Accounts, and Transactions data with embedded fraud patterns.
- **Database Design:** Create a normalized relational schema using MySQL with appropriate constraints.
- **Anomaly Detection:** Train a rule-based fraud detection model using Python on transactional behavior.
- **Interactive Dashboard:** Design a Power BI dashboard for transaction analysis and fraud reporting.

## **Methodology**

### 1. Data Generation with Python

- Utilized the `Faker` library to simulate realistic users, account types, and thousands of transactions.
- Injected fraud-like patterns (e.g. rapid transactions, failed attempts, abnormal values) into the dataset.

### 2. MySQL Relational Database

- Built and populated a banking schema: `Users`, `Accounts`, and `Transactions`.
- Ensured referential integrity with foreign keys and normalized table relationships.

### 3. Fraud Detection Notebook

- Applied a rule-based ML pipeline using `pandas` in Python to detect:
  - High-frequency transactions in short timeframes.
  - Outlier amounts and invalid geographic patterns.
  - Failed login attempts preceding large transactions.
- Flagged suspicious transactions and created labels for Power BI visualization.

### 4. Power BI Dashboard

- Created an executive overview with KPIs like Fraud Rate, Flagged Transactions, and Account Risk Level.
- Visualized:
  - Suspicious activity by user and region.
  - Transaction flows over time.
  - Fraud trends based on behavior patterns and flagged alerts.

## **Key Insights**

- Identified a group of users with above-average fraud risk based on rapid transaction patterns.
- Certain time windows (early morning hours) showed elevated flagged activity.
- Accounts with more than 5 failed login attempts had a 3x higher probability of fraudulent behavior.
- The dashboard enabled real-time investigation into high-risk users and unusual transaction flows.

### **Technologies Used**

- `Python`: Data generation, fraud detection model, EDA.
- `MySQL`: Relational database design and population.
- `Power BI`: Interactive visualizations and executive dashboard.

## **Conclusion**

This project integrates **data engineering**, **machine learning**, and **data visualization** to build a complete banking fraud detection system. It demonstrates the ability to simulate data pipelines, apply intelligent rules for anomaly detection, and empower decision-makers with actionable insights through dashboards. Financial institutions can use similar systems for fraud prevention, compliance, and risk management.

## Power BI link:
[Banking Fraud Dashboard](https://app.powerbi.com/view?r=YOUR_LINK_HERE)

### [Back](https://joaquingf74.github.io/Portfolio/Projects.html)
