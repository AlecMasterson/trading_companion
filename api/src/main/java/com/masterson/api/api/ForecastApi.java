package com.masterson.api.api;

import com.masterson.api.model.forecast.Forecast;
import com.masterson.api.model.Source;
import com.masterson.api.repo.ForecastRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/forecast")
@Slf4j
public class ForecastApi {

    private final ForecastRepository repository;

    @Autowired
    public ForecastApi(ForecastRepository repository) {
        this.repository = repository;
    }

    @GetMapping("/get")
    public List<Forecast> getForecastsBySourceAndTicker(@RequestParam Source source, @RequestParam String ticker) {
        log.info("method=getForecastsBySourceAndTicker, source={} ticker={}", source, ticker);
        return this.repository.findAllBySourceAndTicker(source, ticker);
    }

    @PostMapping("/save")
    public void saveForecasts(@RequestBody List<Forecast> forecasts) {
        log.info("method=saveForecasts, forecasts.size={}", forecasts.size());
        this.repository.saveAll(forecasts);
    }
}
