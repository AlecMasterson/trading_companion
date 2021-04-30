package com.masterson.api.api;

import com.masterson.api.BaseUnitTest;
import com.masterson.api.model.Source;
import com.masterson.api.model.forecast.Forecast;
import com.masterson.api.repo.ForecastRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InOrder;
import org.mockito.Mock;

import java.util.List;

import static com.masterson.api.model.Source.*;
import static java.util.Collections.emptyList;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

public class ForecastApiTest extends BaseUnitTest {

    @Mock
    private ForecastRepository forecastRepository;

    private InOrder callOrder;
    private ForecastApi forecastApi;

    @BeforeEach
    public void init() {
        forecastApi = new ForecastApi(forecastRepository);
        callOrder = inOrder(forecastRepository);

        when(forecastRepository.findAllBySourceAndTicker(isA(Source.class), isA(String.class))).thenReturn(FORECASTS);
    }

    @AfterEach
    public void exit() {
        callOrder.verifyNoMoreInteractions();
    }

    @Test
    public void findAllBySourceAndTickerTest() {
        List<Forecast> forecasts = forecastApi.getForecastsBySourceAndTicker(BINANCE, TICKER_1);
        forecastApi.getForecastsBySourceAndTicker(COINBASE, TICKER_2);

        callOrder.verify(forecastRepository, times(1)).findAllBySourceAndTicker(BINANCE, TICKER_1);
        callOrder.verify(forecastRepository, times(1)).findAllBySourceAndTicker(COINBASE, TICKER_2);

        assertEquals(FORECASTS, forecasts);
    }

    @Test
    public void saveForecastsTest() {
        forecastApi.saveForecasts(emptyList());
        forecastApi.saveForecasts(FORECASTS);

        callOrder.verify(forecastRepository, times(1)).saveAll(emptyList());
        callOrder.verify(forecastRepository, times(1)).saveAll(FORECASTS);
    }
}
