package com.masterson.api;

import com.masterson.api.model.Candle;
import com.masterson.api.model.Interval;
import com.masterson.api.model.forecast.Forecast;

import java.util.List;

import static java.util.Arrays.asList;
import static java.util.Collections.singletonList;

public class BaseTest {
    protected final String TICKER_1 = "ticker-1";
    protected final String TICKER_2 = "ticker-2";
    protected final Interval INTERVAL_1 = Interval.DAY_1;
    protected final Interval INTERVAL_2 = Interval.HOUR_1;
    protected final List<Candle> CANDLES = singletonList(Candle.builder().build());
    protected final List<Forecast> FORECASTS = asList(new Forecast(), new Forecast());
    protected final List<String> TICKERS = asList(TICKER_1, TICKER_2);
}
