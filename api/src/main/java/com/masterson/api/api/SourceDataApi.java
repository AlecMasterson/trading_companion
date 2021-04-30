package com.masterson.api.api;

import com.masterson.api.model.Candle;
import com.masterson.api.model.Interval;
import com.masterson.api.model.Source;
import com.masterson.api.service.SourceDataService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/source")
@Slf4j
public class SourceDataApi {

    private final SourceDataService sourceDataService;

    @Autowired
    public SourceDataApi(SourceDataService sourceDataService) {
        this.sourceDataService = sourceDataService;
    }

    @GetMapping("/get/candles")
    public List<Candle> getCandles(@RequestParam Source source, @RequestParam String ticker, @RequestParam Interval interval) {
        log.info("method=getCandles, source={} ticker={} interval={}", source, ticker, interval);
        return this.sourceDataService.getCandles(source, ticker, interval);
    }

    @GetMapping("/get/tickers")
    public List<String> getTickers(@RequestParam Source source) {
        log.info("method=getTickers, source={}", source);
        return this.sourceDataService.getTickers(source);
    }
}
