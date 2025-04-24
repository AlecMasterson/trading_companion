CREATE SCHEMA IF NOT EXISTS market_data;

CREATE USER ep_senex WITH PASSWORD 'superspecialproductionpassword123';
CREATE USER ep_senex_r WITH PASSWORD 'password123';

GRANT CONNECT ON DATABASE trading_companion TO ep_senex, ep_senex_r;

ALTER ROLE ep_senex SET search_path TO market_data;
ALTER ROLE ep_senex_r SET search_path TO market_data;

GRANT USAGE ON SCHEMA market_data TO ep_senex, ep_senex_r;

GRANT SELECT ON ALL TABLES IN SCHEMA market_data TO ep_senex_r;
ALTER DEFAULT PRIVILEGES IN SCHEMA market_data GRANT SELECT ON TABLES TO ep_senex_r;

GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA market_data TO ep_senex;
ALTER DEFAULT PRIVILEGES IN SCHEMA market_data GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO ep_senex;

CREATE TABLE market_data.candles (
	source VARCHAR(20) NOT NULL,
	ticker VARCHAR(20) NOT NULL,
	granularity VARCHAR(20) NOT NULL,
	timestamp TIMESTAMPTZ NOT NULL,
	close NUMERIC NOT NULL,
	high NUMERIC NOT NULL,
	low NUMERIC NOT NULL,
	open NUMERIC NOT NULL,
	volume NUMERIC NOT NULL,
	created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
	updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
	CONSTRAINT candles_pk PRIMARY KEY (source, ticker, granularity, timestamp)
);

CREATE TABLE market_data.tickers (
	ticker VARCHAR(20) NOT NULL,
	name TEXT NOT NULL,
	type VARCHAR(20) NOT NULL,
	created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
	updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
	CONSTRAINT tickers_pk PRIMARY KEY (ticker)
);
