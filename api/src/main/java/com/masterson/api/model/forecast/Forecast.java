package com.masterson.api.model.forecast;

import com.masterson.api.model.BaseEntity;
import com.masterson.api.model.Interval;
import com.masterson.api.model.Source;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.IdClass;

@Entity(name = "FORECAST")
@IdClass(ForecastId.class)
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Forecast extends BaseEntity {

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

    @Column(name = "PRICE")
    private float price;

    @Column(name = "PRICE_C")
    private float correctPrice;
}
