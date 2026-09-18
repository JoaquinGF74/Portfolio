-- ============================================================
-- Athlete Workload & Injury-Risk Analytics — schema (PostgreSQL)
-- Players -> Sessions (training/match load) -> computed risk scores
-- Power BI connects directly to this database; no CSV hand-off.
-- ============================================================

CREATE TABLE Players (
	player_id		SERIAL PRIMARY KEY,
	full_name		VARCHAR(100) NOT NULL,
	position		VARCHAR(30) NOT NULL, -- e.g. "prop", "winger", "scrum-half"
	team			VARCHAR(50) NOT NULL,
	date_of_birth	DATE
);

CREATE TABLE Sessions (
	session_id			SERIAL PRIMARY KEY,
	player_id			INT NOT NULL REFERENCES Players(player_id),
	session_date		DATE NOT NULL,
	session_type		VARCHAR(20) NOT NULL,	--"training" or "match"
	duration_minutes	INT NOT NULL,
	rpe					SMALLINT NOT NULL,		-- Rate of Perceived Exertion, 1-10 (Borg CR10 sacle)
	distance_km			DECIMAL(5,2),
	high_speed_m		INT						-- meters covered above high-speed running threshhold
);

-- Populated by the Python pipeline afgter computing ACWR + Risk flags.
-- Power BI reads this table directly for the dashboard
CREATE TABLE PlayerRiskScore (
	score_id			SERIAL PRIMARY KEY,
	player_id			INT NOT NULL REFERENCES Players(player_id),
	as_of_date			DATE NOT NULL,
	acute_workload		DECIMAL(8,2), 	-- rolling 7-day load (duration * RPE, summed)
	chronic_workload	DECIMAL(8,2), 	-- rolling 28-day  average weekly load
	acwr				DECIMAL(8,2), 	-- acute:chronic workload ratio
	risk_flag			VARCHAR(20)		-- "low", "moderate", "high", "insufficient_data"
);

CREATE INDEX idx_sessions_player_date ON Sessions(player_id, session_date);