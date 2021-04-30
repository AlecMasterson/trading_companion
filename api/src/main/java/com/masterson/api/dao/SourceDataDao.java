package com.masterson.api.dao;

import com.masterson.api.model.Interval;
import com.masterson.api.model.Source;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;

import java.util.List;
import java.util.Map;

import static com.masterson.api.model.Source.*;
import static java.util.Collections.singletonList;

@Repository
public class SourceDataDao {

    private final Map<Source, SourceDataDaoProps> CANDLE_CONFIG = Map.of(
            BINANCE, new SourceDataDaoProps("/api/v3/klines", SourceDataDao::buildBinanceCandleParams, null),
            COINBASE, new SourceDataDaoProps("/products/{ticker}/candles", null, SourceDataDao::buildCoinbaseCandleArgs));
    private final Map<Source, SourceDataDaoProps> TICKER_CONFIG = Map.of(
            BINANCE, new SourceDataDaoProps("/api/v3/exchangeInfo", null, null),
            COINBASE, new SourceDataDaoProps("/products", null, null));

    private final WebClientDao webClient;

    @Autowired
    public SourceDataDao(WebClientDao webClient) {
        this.webClient = webClient;
    }

    public List<List<Object>> getCandles(Source source, String ticker, Interval interval) {
        SourceDataDaoProps props = CANDLE_CONFIG.get(source);
        ParamsBuilderFunc paramsBuilderFunc = props.getParamsBuilderFunc();
        ArgsBuilderFunc argsBuilderFunc = props.getArgsBuilderFunc();

        return webClient.getItems(props.getPath(),
                paramsBuilderFunc != null ? paramsBuilderFunc.build(ticker, interval) : null,
                argsBuilderFunc != null ? argsBuilderFunc.build(ticker, interval) : null);
    }

    public List<String> getTickers(Source source) {
        SourceDataDaoProps props = TICKER_CONFIG.get(source);
        ParamsBuilderFunc paramsBuilderFunc = props.getParamsBuilderFunc();
        ArgsBuilderFunc argsBuilderFunc = props.getArgsBuilderFunc();

        return webClient.getItems(props.getPath(),
                paramsBuilderFunc != null ? paramsBuilderFunc.build(null, null) : null,
                argsBuilderFunc != null ? argsBuilderFunc.build(null, null) : null);
    }

    private static MultiValueMap<String, String> buildBinanceCandleParams(String ticker, Interval interval) {
        MultiValueMap<String, String> requestParams = new LinkedMultiValueMap<>();
        requestParams.put("ticker", singletonList(ticker));
        requestParams.put("interval", singletonList(interval.name()));

        return requestParams;
    }

    private static Object[] buildCoinbaseCandleArgs(String ticker, Interval interval) {
        return new String[]{ticker};
    }

    @AllArgsConstructor
    @Getter
    private static class SourceDataDaoProps {
        private final String path;
        private final ParamsBuilderFunc paramsBuilderFunc;
        private final ArgsBuilderFunc argsBuilderFunc;
    }

    private interface ParamsBuilderFunc {
        MultiValueMap<String, String> build(String ticker, Interval interval);
    }

    private interface ArgsBuilderFunc {
        Object[] build(String ticker, Interval interval);
    }
}
