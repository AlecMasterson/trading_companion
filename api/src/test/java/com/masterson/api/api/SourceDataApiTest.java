package com.masterson.api.api;

import com.masterson.api.BaseUnitTest;
import com.masterson.api.model.Candle;
import com.masterson.api.model.Interval;
import com.masterson.api.model.Source;
import com.masterson.api.service.SourceDataService;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InOrder;
import org.mockito.Mock;

import java.util.List;

import static com.masterson.api.model.Source.*;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

public class SourceDataApiTest extends BaseUnitTest {

    @Mock
    private SourceDataService sourceDataService;

    private InOrder callOrder;
    private SourceDataApi sourceDataApi;

    @BeforeEach
    public void init() {
        sourceDataApi = new SourceDataApi(sourceDataService);
        callOrder = inOrder(sourceDataService);

        when(sourceDataService.getCandles(isA(Source.class), isA(String.class), isA(Interval.class)))
                .thenReturn(CANDLES);
        when(sourceDataService.getTickers(isA(Source.class))).thenReturn(TICKERS);
    }

    @AfterEach
    public void exit() {
        callOrder.verifyNoMoreInteractions();
    }

    @Test
    public void getCandlesTest() {
        List<Candle> candles = sourceDataApi.getCandles(BINANCE, TICKER_1, INTERVAL_1);
        sourceDataApi.getCandles(COINBASE, TICKER_2, INTERVAL_2);

        callOrder.verify(sourceDataService, times(1)).getCandles(BINANCE, TICKER_1, INTERVAL_1);
        callOrder.verify(sourceDataService, times(1)).getCandles(COINBASE, TICKER_2, INTERVAL_2);

        assertEquals(CANDLES, candles);
    }

    @Test
    public void getTickersTest() {
        List<String> tickers = sourceDataApi.getTickers(BINANCE);
        sourceDataApi.getTickers(COINBASE);

        callOrder.verify(sourceDataService, times(1)).getTickers(BINANCE);
        callOrder.verify(sourceDataService, times(1)).getTickers(COINBASE);

        assertEquals(TICKERS, tickers);
    }
}
