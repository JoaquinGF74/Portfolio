"""
Athlete Workload & Injury-Risk Pipeline (PostgreSQL version)
Generates realistic session data -> stores in PostgreSQL -> computes ACWR in Python
-> writes risk scores back into the SAME database for Power BI to consume directly.
"""

import psycopg2
import pandas as pd
import numpy as np
from acwr_logic import compute_acwr

import os
from dotenv import load_dotenv

load_dotenv()  # reads the .env file into environment variables

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

# 2. Seed Players (skip if already populated)

position = ["Prop", "Hooker", "Lock", "Flanker", "Number 8", 
            "Scrum-half", "Fly-half", "Centre", "Wing", "Fullback"]

cursor.execute("SELECT COUNT(*) FROM Players")
existing_player_count = cursor.fetchone()[0]
rng = np.random.default_rng()

if existing_player_count == 0:
    players = [ # generate 80 players with random positions and birthdates
        (f"Player {i}", position[i % len(position)], "Saint Thomas University", # assign position in a round-robin fashion
        f"20{rng.integers(0, 4):02d}-{rng.integers(1, 13):02d}-{rng.integers(1, 29):02d}") # random birthdate between 2000 and 2003
        for i in range(1,81)
    ]

    cursor.executemany( # insert generated players into the Players table
        "INSERT INTO Players (full_name, position, team, date_of_birth) VALUES (%s, %s, %s, %s)", 
        players
    )
    conn.commit() # commit the transaction to save changes to the database
    print(f"Seeded {len(players)} new players") # print the number of players seeded
else:
    print(f"Players already seeded ({existing_player_count} found) - Skipping.")

cursor.execute("SELECT player_id, position FROM Players") # fetch all players to verify insertion
player_rows = cursor.fetchall()
player_ids = [row[0] for row in player_rows]
player_positions = {row[0]: row[1] for row in player_rows}

FORWARD_POSITION = {"Prop", "Hooker", "Lock", "Flanker", "Number 8"}

# 3. Generate 90 days of realistic training/match sessions

last_session_date = pd.read_sql("SELECT MAX(session_date) FROM Sessions", conn).iloc[0,0] # get the most recent session date from the Sessions table
if last_session_date is None:
    last_session_date = pd.Timestamp.today().normalize() # if no sessions exist, use the current date
    dates = pd.date_range(last_session_date - pd.Timedelta("7D"), periods=7, freq="D")
else:  
    last_session_date = pd.Timestamp(last_session_date) # convert to Timestamp for consistency
    dates = pd.date_range(last_session_date + pd.Timedelta("1D"), periods=7, freq="D") # generate 90 days of sessions starting from the day after the last session
session_rows = []

for pid in player_ids:
    is_forward = player_positions[pid] in FORWARD_POSITION
    base_rpe = rng.integers(4, 7)
    for d in dates:
            is_match_day = d.weekday() == 5
            if is_match_day or rng.random() < 0.55:
                duration = int(rng.integers(70, 100)) if is_match_day else int(rng.integers(40, 80))
                rpe = min(10, base_rpe + rng.integers(0, 4) + (2 if is_match_day else 0))
                if is_match_day:
                    if is_forward:
                        distance = round(rng.uniform(5.0, 6.0), 2)
                        high_speed = int(rng.integers(100, 251))
                    else:
                        distance = round(rng.uniform(6.0, 7.5), 2)
                        high_speed = int(rng.integers(250, 451))
                else:
                    if is_forward:
                        distance = round(rng.uniform(3.0, 4.5), 2)
                        high_speed = int(rng.integers(300, 451))
                    else:
                        distance = round(rng.uniform(4.0, 6.5), 2)
                        high_speed = int(rng.integers(450, 601))
                session_rows.append((
                    pid, d.date(), "match" if is_match_day else "training", 
                    duration, int(rpe), distance, high_speed
                ))
                    
cursor.executemany( # insert generated session data into the Sessions table
    """INSERT INTO Sessions
            (player_id, session_date, session_type, duration_minutes, rpe, distance_km, high_speed_m)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (player_id, session_date, session_type)
        DO UPDATE SET
            duration_minutes = EXCLUDED.duration_minutes,
            rpe = EXCLUDED.rpe,
            distance_km = EXCLUDED.distance_km,
            high_speed_m = EXCLUDED.high_speed_m
    """, session_rows  
)
conn.commit() # commit the transaction to save changes to the database

# 4. Pull sessions back, compute ACWR in Python (single source of truth)

sessions_df = pd.read_sql(
    "SELECT player_id, session_date, duration_minutes, rpe FROM Sessions",
    conn
)
risk_df = compute_acwr(sessions_df) # compute ACWR using the imported function

# only keep rows where we have enough history to trust the number
risk_df = risk_df[risk_df["risk_flag"] != "insufficient_data"]

# 5. Write results back into the SAME database -> Power BI connects live to PlayerRiskScore, no CSV hand-off

# prepare the SQL statement for inserting risk scores into the PlayerRiskScore table
insert_scores = """ INSERT INTO PlayerRiskScore
        (player_id, as_of_date, acute_workload, chronic_workload, acwr, risk_flag)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (player_id, as_of_date)
    DO UPDATE SET
        acute_workload = EXCLUDED.acute_workload,
        chronic_workload = EXCLUDED.chronic_workload,
        acwr = EXCLUDED.acwr,
        risk_flag = EXCLUDED.risk_flag """ 
# convert the DataFrame to a list of tuples for insertion
score_rows = list(risk_df[ 
    ["player_id", "as_of_date", "acute_workload", "chronic_workload", "acwr", "risk_flag"]
    ].itertuples(index=False, name=None))

cursor.executemany(insert_scores, score_rows) # execute the insertion of risk scores
conn.commit() # commit the transaction to save changes to the database

print(f"Inserted {len(player_ids)} players,  {len(session_rows)} sessions, "
      f"{len(score_rows)} risk-score rows.")
print("\nCurrent high-risk players*(most recent date):")
latest_date = risk_df["as_of_date"].max() # find the most recent date in the risk DataFrame
print(risk_df[(risk_df["as_of_date"] == latest_date) & (risk_df["risk_flag"] == "high")]) # print the top 10 high-risk players for the most recent date

cursor.close()
conn.close()