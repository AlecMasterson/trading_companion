-- create database trading_companion
-- with
-- owner = my_user
-- encoding = 'UTF-8'
-- tablespace = pg_default;

DROP SCHEMA public CASCADE;

-- DROP SCHEMA stocks;

CREATE SCHEMA stocks AUTHORIZATION ep_senex;


-- DROP TABLE stocks.history;

CREATE TABLE stocks.history (
	ticker varchar(10) NOT NULL,
	"timestamp" timestamptz NOT NULL,
	granularity varchar(10) NOT NULL,
	"close" numeric NOT NULL,
	high numeric NOT NULL,
	low numeric NOT NULL,
	"open" numeric NOT NULL,
	volume numeric NOT NULL,
	CONSTRAINT history_pk PRIMARY KEY (ticker, "timestamp", "granularity")
);

-- DROP TABLE stocks.ticker;

CREATE TABLE stocks.ticker (
	ticker VARCHAR(10) NOT NULL,
	"name" TEXT NOT NULL,
	exchange VARCHAR(10) NOT NULL,
	"type" VARCHAR(10) NOT NULL,
	market_cap NUMERIC DEFAULT 0 NOT NULL,
	active BOOLEAN DEFAULT false NOT NULL,
	last_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "valid" BOOLEAN DEFAULT false NOT NULL,
	CONSTRAINT ticker_pk PRIMARY KEY (ticker)
);
