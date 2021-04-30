package com.masterson.api.dao;

import com.masterson.api.BaseUnitTest;
import com.masterson.api.model.Interval;
import com.masterson.api.model.Source;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;

import static java.util.Collections.singletonList;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.*;

public class SourceDataDaoTest extends BaseUnitTest {

    @Mock
    private WebClientDao webClientDao;

    private final String TICKER = "ticker-1";
    private final Interval INTERVAL = Interval.DAY_1;

    private SourceDataDao sourceDataDao;

    @BeforeEach
    public void init() {
        sourceDataDao = new SourceDataDao(webClientDao);
    }

    @AfterEach
    public void exit() {
        verifyNoMoreInteractions(webClientDao);
    }

    @Test
    public void getCandlesNull() {
        assertThrows(NullPointerException.class, () -> {
            sourceDataDao.getCandles(null, TICKER, INTERVAL);
        });

        verifyNoInteractions(webClientDao);
    }

    @Test
    public void getCandlesBinance() {
        MultiValueMap<String, String> expectedParams = new LinkedMultiValueMap<>();
        expectedParams.put("ticker", singletonList(TICKER));
        expectedParams.put("interval", singletonList(INTERVAL.name()));

        sourceDataDao.getCandles(Source.BINANCE, TICKER, INTERVAL);

        verify(webClientDao, times(1)).getItems("/api/v3/klines", expectedParams, (Object) null);
    }

    @Test
    public void getCandlesCoinbase() {
        sourceDataDao.getCandles(Source.COINBASE, TICKER, INTERVAL);

        verify(webClientDao, times(1)).getItems("/products/{ticker}/candles", null, TICKER);
    }

    @Test
    public void getTickersNull() {
        assertThrows(NullPointerException.class, () -> {
            sourceDataDao.getTickers(null);
        });

        verifyNoInteractions(webClientDao);
    }

    @Test
    public void getTickersBinance() {
        sourceDataDao.getTickers(Source.BINANCE);

        verify(webClientDao, times(1)).getItems("/api/v3/exchangeInfo", null, (Object) null);
    }

    @Test
    public void getTickersCoinbase() {
        sourceDataDao.getTickers(Source.COINBASE);

        verify(webClientDao, times(1)).getItems("/products", null, (Object) null);
    }
}
