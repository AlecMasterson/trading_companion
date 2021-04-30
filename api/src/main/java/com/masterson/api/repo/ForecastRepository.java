package com.masterson.api.repo;

import com.masterson.api.model.forecast.Forecast;
import com.masterson.api.model.forecast.ForecastId;
import com.masterson.api.model.Source;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ForecastRepository extends CrudRepository<Forecast, ForecastId> {
    List<Forecast> findAllBySourceAndTicker(Source source, String ticker);
}
