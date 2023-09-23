CREATE TABLE conditions(
    time TIMESTAMPTZ NOT NULL,
    device INTEGER,
    temperature FLOAT
);

SELECT * FROM create_hypertable('conditions', 'time', chunk_time_interval => INTERVAL '1 day');

INSERT INTO conditions
SELECT time, (random()*30)::int, random()*80 - 40
FROM generate_series(now() - '1 month'::interval,
     		     now(),
		     INTERVAL '1 min') AS time;

CREATE MATERIALIZED VIEW conditions_summary_hourly
WITH (timescaledb.continuous) AS
SELECT device,
       time_bucket('1 hour', "time") AS bucket,
       AVG(temperature),
       MAX(temperature),
       MIN(temperature)
FROM conditions
GROUP BY device, bucket
WITH NO DATA;

SELECT drop_chunks('conditions', now() - '2 weeks'::interval);
