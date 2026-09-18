import pandas as pd
import numpy as np

def compute_acwr(sessions: pd.DataFrame) -> pd.DataFrame:
    """
    sessions: DataFrame with columns [player_id, session_date, duration_minutes, rpe]
    Returns one row per (player_id, as_of_date) with acute/chronic workload, ACWR, risk_flag.

    Method: rolling-average ACWR (Gabbett, 2016) —
      acute_workload   = sum of session load (duration * RPE) over trailing 7 days
      chronic_workload = average *weekly* load over trailing 28 days (chronic / 4)
      acwr             = acute_workload / chronic_workload
    Risk bands (established in sports-science literature):
      ACWR < 0.8            -> 'low'      (undertrained, not itself dangerous but flagged)
      0.8 <= ACWR <= 1.3     -> 'low'      (the "sweet spot")
      1.3 < ACWR <= 1.5      -> 'moderate'
      ACWR > 1.5             -> 'high'     (sharp spike in load, elevated injury risk)
    """
    df = sessions.copy() # make a copy to avoid modifying the original DataFrame
    df["session_date"] = pd.to_datetime(df["session_date"]) # ensure session_date is a datetime type for proper resampling and rolling calculations
    df["load"] = df["duration_minutes"] * df["rpe"] # compute session load as duration * RPE

    results = [] # list of dicts to be converted to DataFrame at the end
    for player_id, g in df.groupby("player_id"): # group by player_id to compute ACWR for each player separately
        g = g.set_index("session_date").sort_index() # sort by session_date to ensure rolling windows are correct
        daily_load = g["load"].resample("D").sum().fillna(0) # resample to daily load, filling missing days with 0 load

        acute = daily_load.rolling("7D").sum() # total load over trailing 7 days
        chronic_28d_total = daily_load.rolling("28D").sum() # total load over trailing 28 days
        chronic_weekly_avg = chronic_28d_total / 4  # average weekly load over trailing 28 days
        days_of_data = daily_load.rolling("28D").count() # count of days with data in the trailing 28 days

        acwr = (acute / chronic_weekly_avg).replace([np.inf, -np.inf], np.nan) # compute ACWR, handling division by zero

        for date, a, c, r, d in zip(daily_load.index, acute, chronic_weekly_avg, acwr, days_of_data): # iterate over each date to create a row in the results
            if pd.isna(r) | (d < 28): # if we don't have enough data to compute a reliable ACWR, flag as insufficient_data
                risk = 'insufficient_data'
            elif r > 1.5: # if ACWR is greater than 1.5, risk is high
                risk = 'high'
            elif r > 1.3: # if ACWR is between 1.3 and 1.5, risk is moderate
                risk = 'moderate'
            elif r >= 0.8: # if ACWR is between 0.8 and 1.3, risk is low
                risk = 'low'
            else: # if ACWR is less than 0.8, risk is low (undertrained)
                risk = 'low'

            results.append({ # create a dictionary for this row with the computed values
                "player_id": player_id,
                "as_of_date": date.date(),
                "acute_workload": round(a, 2),
                "chronic_workload": round(c, 2) if not pd.isna(c) else None,
                "acwr": round(r, 2) if not pd.isna(r) else None,
                "risk_flag": risk
            })
    return pd.DataFrame(results) # convert the list of dicts to a DataFrame and return

if __name__ == "__main__":
    # Quick sanity check with synthetic data before this ever touches a real DB
    rng = np.random.default_rng(42)
    dates = pd.date_range("2026-01-01", periods = 60, freq="D")
    rows = []
    for player_id in [1, 2]: # simulate two players
        for d in dates:
            if rng.random() < 0.6: # 60% chance of having a session on a given day
                rows.append({
                    "player_id": player_id,
                    "session_date": d,
                    "duration_minutes": rng.integers(30, 90), # random duration between 30 and 90 minutes
                    "rpe": rng.integers(3, 9) # random RPE between 3 and 9
                })
    # simulate player 2 having a sudden spike in the last week (injury-risk scenario)     
    for d in dates[-7:]:
        rows.append({
            "player_id": 2,
            "session_date": d,
            "duration_minutes": 90,
            "rpe": 9
        })

    sessions_df = pd.DataFrame(rows) # create a DataFrame from the synthetic data
    result = compute_acwr(sessions_df) # compute ACWR on the synthetic data
    print(result.tail(10)) # print the resulting DataFrame to verify the output
    print("\nRisk flag distribution:\n", result["risk_flag"].value_counts()) # print the distribution of risk flags to see how many sessions fall into each risk category