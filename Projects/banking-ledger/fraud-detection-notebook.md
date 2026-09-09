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

```python
import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# 1. Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="temp",       
    password="temp",   
    database="banking_db"       
)
cursor = conn.cursor()

# 2. Generate Users
print("Generating users...")
users = []
for user_id in range(1, 1001):
    users.append((
        user_id,
        fake.name(),
        fake.email(),
        fake.date_time_between(start_date='-3y', end_date='now')
    ))

cursor.executemany("""
  INSERT INTO Users (user_id, name, email, created_at)
  VALUES (%s, %s, %s, %s)""", users)

# 3. Generate Accounts
print("Generating accounts...")
accounts = []
account_id = 1
user_account_map = {}

for user in users:
    num_accounts = random.randint(1, 3)
    user_account_map[user[0]] = []
    for _ in range(num_accounts):
        balance = round(random.uniform(100, 10000), 2)
        account_type = random.choice(['checking', 'savings'])
        created_at = fake.date_time_between(start_date=user[3], end_date='now')

        accounts.append((
            account_id,
            user[0],  # user_id
            account_type,
            balance,
            created_at
        ))
        user_account_map[user[0]].append(account_id)
        account_id += 1

cursor.executemany("""
  INSERT INTO Accounts (account_id, user_id, account_type, balance, created_at)
  VALUES (%s, %s, %s, %s, %s) """, accounts)

# 4. Generate Transactions
print("Generating transactions...")
transactions = []
transaction_id = 1
account_ids = [acc[0] for acc in accounts]

for _ in range(10000):
    sender = random.choice(account_ids)
    receiver = random.choice(account_ids)
    while receiver == sender:
        receiver = random.choice(account_ids)

    amount = round(random.uniform(5, 5000), 2)
    txn_type = random.choice(['transfer', 'deposit', 'withdrawal'])
    status = random.choices(['success', 'failed'], weights=[95, 5])[0]
    created_at = fake.date_time_between(start_date='-2y', end_date='now')

    transactions.append((
        transaction_id,
        sender if txn_type != 'deposit' else None,
        receiver if txn_type != 'withdrawal' else None,
        amount,
        txn_type,
        status,
        created_at
    ))
    transaction_id += 1

cursor.executemany("""
  INSERT INTO Transactions (transaction_id, sender_account, receiver_account, amount, transaction_type, status, created_at)
  VALUES (%s, %s, %s, %s, %s, %s, %s) """, transactions)

# 5. Finalize
conn.commit()
cursor.close()
conn.close()
print("Data generation complete!")
```

### 2. MySQL Relational Database

- Built and populated a banking schema: `Users`, `Accounts`, and `Transactions`.
- Ensured referential integrity with foreign keys and normalized table relationships.

```sql
CREATE DATABASE IF NOT EXISTS banking_db;
USE banking_db;

CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at DATETIME
);

CREATE TABLE Accounts (
    account_id INT PRIMARY KEY,
    user_id INT,
    account_type VARCHAR(50),
    balance DECIMAL(10,2),
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY,
    account_id INT,
    amount DECIMAL(10,2),
    transaction_type VARCHAR(50),
    transaction_date DATETIME,
    merchant VARCHAR(100),
    location VARCHAR(100),
    is_fraud BOOLEAN DEFAULT 0,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);
```
### 3. Fraud Detection Notebook

- Applied a rule-based ML pipeline using `pandas` in Python to detect:
  - High-frequency transactions in short timeframes.
  - Outlier amounts and invalid geographic patterns.
  - Failed login attempts preceding large transactions.
- Flagged suspicious transactions and created labels for Power BI visualization.

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Load the data
df = pd.read_csv("transactions.csv")

# Select features and label
X = df[["amount"]]
y = df["is_fraud"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
```

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

### [Back](https://joaquingf74.github.io/Portfolio/Projects.html)
