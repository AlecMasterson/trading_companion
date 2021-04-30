package com.masterson.api.model.forecast;

import com.masterson.api.model.Interval;
import com.masterson.api.model.Source;
import lombok.Getter;

import javax.persistence.Column;
import javax.persistence.Id;
import java.io.Serializable;

@Getter
public class ForecastId implements Serializable {

    @Id
    @Column(name = "SOURCE")
    private Source source;

    @Id
    @Column(name = "TICKER")
    private String ticker;

    @Id
    @Column(name = "TIME_INTERVAL")
    private Interval interval;

    @Id
    @Column(name = "FUTURE_TIME")
    private String futureTime;
}
