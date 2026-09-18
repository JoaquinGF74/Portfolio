Commands used

Created Database: 
psql -U postgres -h localhost -d postgres -c "CREATE DATABASE athlete_schema;"
Load schema: 
psql -U postgres -h localhost -d athlete_schema -f athlete_schema.sql

Add constraints:
psql -U postgres -h localhost -d athlete_schema -c "ALTER TABLE Sessions ADD CONSTRAINT uq_player_session UNIQUE (player_id, session_date, session_type);"
psql -U postgres -h localhost -d athlete_schema -c "ALTER TABLE PlayerRiskScore ADD CONSTRAINT uq_player_date UNIQUE (player_id, as_of_date);"

Run pipeline:
python3 run_pipeline.py

Some queries:
Last player's session.
psql -U postgres -h localhost -d athlete_schema -c "SELECT Sessions.player_id, MAX(session_date) FROM Sessions GROUP BY Sessions.player_id ORDER BY Sessions.player_id;"

Highest acwr score by player to record.
psql -U postgres -h localhost -d athlete_schema -c "SELECT p.player_id, MAX(acwr) FROM PlayerRiskScore AS p GROUP BY p.player_id ORDER BY p.player_id;"

